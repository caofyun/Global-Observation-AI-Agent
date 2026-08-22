from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
import json
import os
import re
from urllib.parse import urlsplit, urlunsplit

from src.agents.base_agent import BaseAgent
from src.utils.search_tool import SearchTool


class NewsDiscovery(BaseAgent):
    """News Discovery V2.1 MVP."""

    SEARCH_TIME_OPERATORS = {
        "1h": "when:1h",
        "6h": "when:6h",
        "12h": "when:12h",
        "24h": "when:1d",
        "48h": "when:2d",
        "7d": "when:7d",
    }

    SUPPORTED_TIME_RANGES = {
        "1h": timedelta(hours=1),
        "6h": timedelta(hours=6),
        "12h": timedelta(hours=12),
        "24h": timedelta(hours=24),
        "48h": timedelta(hours=48),
        "7d": timedelta(days=7),
    }

    def __init__(self, project_path=None, search_tool=None, now_provider=None):
        super().__init__("NewsDiscovery", project_path)
        self.search_tool = search_tool or SearchTool()
        self.now_provider = now_provider or (lambda: datetime.now(timezone.utc))

    def build_search_queries(self, request):
        topic = request["topic"]
        time_operator = self.SEARCH_TIME_OPERATORS[request["time_range"]]
        domain = request.get("domain")
        geographic_scope = request.get("geographic_scope") or []
        focus_areas = request.get("focus_areas") or []
        query_specs = [(topic, "topic", 1)]

        if domain:
            query_specs.append((f"{domain} {topic}", "domain", 1))

        for area in focus_areas:
            query_specs.append((f"{topic} {area}", str(area), 1))

        for location in geographic_scope:
            query_specs.append((f"{location} {topic}", str(location), 2))

        query_specs.append((f"{topic} 最新消息", "latest", 1))

        queries = []
        seen_queries = set()
        for query, category, priority in query_specs:
            query = str(query).strip()
            if not query or query in seen_queries:
                continue
            seen_queries.add(query)
            queries.append({
                "query": f"{query} {time_operator}",
                "category": category,
                "priority": priority,
                "query_index": len(queries) + 1,
            })
        return queries

    @staticmethod
    def _parse_datetime(value):
        if not value:
            return None
        if isinstance(value, datetime):
            parsed = value
        else:
            text = str(value).strip()
            if not text:
                return None
            try:
                parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
            except ValueError:
                try:
                    parsed = parsedate_to_datetime(text)
                except (TypeError, ValueError, OverflowError):
                    return None
        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)

    @staticmethod
    def _normalize_url(url):
        parsed = urlsplit(str(url).strip())
        if parsed.scheme.lower() not in {"http", "https"} or not parsed.netloc:
            return ""
        return urlunsplit((
            parsed.scheme.lower(),
            parsed.netloc.lower(),
            parsed.path or "/",
            parsed.query,
            "",
        ))

    @staticmethod
    def _normalize_title(title):
        return re.sub(r"\s+", " ", str(title).strip()).casefold()

    @staticmethod
    def _as_text(value):
        return "" if value is None else str(value).strip()

    @staticmethod
    def _source_id(source):
        normalized = re.sub(r"[^a-z0-9]+", "_", str(source).strip().casefold()).strip("_")
        return "source_" + (normalized or "unknown")

    def _validate_request(self, request):
        if not isinstance(request, dict):
            raise ValueError("Discovery Request 必须是对象")
        topic = request.get("topic")
        if not isinstance(topic, str) or not topic.strip():
            raise ValueError("topic 必须是非空字符串")
        if request.get("time_range") not in self.SUPPORTED_TIME_RANGES:
            raise ValueError("time_range 无效")
        max_candidates = request.get("max_candidates")
        if isinstance(max_candidates, bool) or not isinstance(max_candidates, int) or max_candidates <= 0:
            raise ValueError("max_candidates 必须是正整数")
        return {
            **request,
            "topic": topic.strip(),
        }

    def _is_in_time_range(self, published_at, time_range, now):
        published = self._parse_datetime(published_at)
        if published is None:
            return False
        return now - self.SUPPORTED_TIME_RANGES[time_range] <= published <= now

    def _normalize_candidate(self, result, query_records, discovered_at, article_index):
        published = self._parse_datetime(result.get("published_time"))
        published_at = published.isoformat() if published else None
        queries = sorted(
            {record["query"] for record in query_records},
            key=lambda query: next(
                record["query_index"] for record in query_records
                if record["query"] == query
            ),
        )
        primary = min(
            query_records,
            key=lambda record: (record["priority"], record["query_index"]),
        )["query"]
        return {
            "article_id": f"ND-{discovered_at[:10].replace('-', '')}-{article_index:06d}",
            "domain": self._as_text(self._current_request.get("domain")) or None,
            "topic": self._current_request["topic"],
            "query": primary,
            "queries": queries,
            "title": self._as_text(result.get("title")),
            "source": self._as_text(result.get("source")),
            "source_id": self._source_id(result.get("source")),
            "url": self._normalize_url(result.get("url")),
            "published_at": published_at,
            "discovered_at": discovered_at,
            "summary": None,
            "content": None,
            "discovery_status": "DISCOVERED",
        }

    def execute(self, input_data):
        request = self._validate_request(input_data)
        self._current_request = request
        now = self._parse_datetime(self.now_provider()) or datetime.now(timezone.utc)
        discovered_at = now.isoformat()
        query_specs = self.build_search_queries(request)
        query_map = {item["query"]: item for item in query_specs}

        raw_results = []
        for query_spec in query_specs:
            results = self.search_tool.search(query_spec["query"], max_results=10)
            if results is None:
                continue
            raw_results.extend(
                (result, query_spec) for result in results if isinstance(result, dict)
            )

        filtered_results = []
        for result, query_spec in raw_results:
            title = self._as_text(result.get("title"))
            source = self._as_text(result.get("source"))
            normalized_url = self._normalize_url(result.get("url"))
            if not title or not source or not normalized_url:
                continue
            if not self._is_in_time_range(
                result.get("published_time"), request["time_range"], now
            ):
                continue
            filtered_results.append((result, query_spec, normalized_url))

        candidates = []
        url_indexes = {}
        title_indexes = {}
        for result, query_spec, normalized_url in filtered_results:
            title_key = self._normalize_title(result.get("title"))
            existing_index = url_indexes.get(normalized_url)
            if existing_index is None:
                existing_index = title_indexes.get(title_key)
            if existing_index is None:
                existing_index = len(candidates)
                candidates.append({
                    "result": result,
                    "query_records": [query_spec],
                })
                url_indexes[normalized_url] = existing_index
                title_indexes[title_key] = existing_index
            else:
                candidates[existing_index]["query_records"].append(query_spec)

        deduplicated_results = len(candidates)
        final_candidates = candidates[:request["max_candidates"]]
        articles = [
            self._normalize_candidate(
                item["result"], item["query_records"], discovered_at, index + 1
            )
            for index, item in enumerate(final_candidates)
        ]
        output = {
            "schema_version": "2.1",
            "status": "SUCCESS",
            "domain": self._as_text(request.get("domain")) or None,
            "topic": request["topic"],
            "discovery": {
                "time_range": request["time_range"],
                "geographic_scope": request.get("geographic_scope") or [],
                "focus_areas": request.get("focus_areas") or [],
                "discovered_at": discovered_at,
                "search_queries": query_specs,
                "query_count": len(query_specs),
            },
            "statistics": {
                "raw_results": len(raw_results),
                "deduplicated_results": deduplicated_results,
                "final_candidates": len(articles),
            },
            "articles": articles,
        }
        self._write_output(output)
        return output

    def _write_output(self, output):
        if not self.project_path:
            return None
        news_folder = os.path.join(self.project_path, "01_新闻资料")
        os.makedirs(news_folder, exist_ok=True)
        output_path = os.path.join(news_folder, "news_articles.json")
        with open(output_path, "w", encoding="utf-8") as output_file:
            json.dump(output, output_file, ensure_ascii=False, indent=4)
        return output_path
