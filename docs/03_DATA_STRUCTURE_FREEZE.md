# V2.0 Data Structure Freeze

## 文档状态

V2.0 Data Structure Freeze
Freeze Approved

---

## 1. 数据结构冻结目标

本文件基于已冻结的 Agent 基线 [docs/01_AGENT_BASELINE_FREEZE.md](docs/01_AGENT_BASELINE_FREEZE.md) 与接口冻结方案 [docs/02_AGENT_INTERFACE_FREEZE.md](docs/02_AGENT_INTERFACE_FREEZE.md)，对当前 V2.0 正式基线中的四类标准输出文件进行字段结构冻结，目标是：

1. 明确冻结 search_results.json、news_articles.json、verification.json、source_rank.json 的标准字段结构。
2. 统一文件命名、字段命名、层级结构与语义边界，避免数据漂移。
3. 形成稳定的输入输出接口契约，保证 Agent 之间的文件交换具备可预测性。
4. 仅保留当前已实现的最小数据结构集合，不扩展未落地的未来结构。
5. 禁止在正式冻结后随意修改字段名、重命名对象层级或改造数据类型。

---

## 2. 冻结范围

本次数据结构冻结范围：

- search_results.json
- news_articles.json
- verification.json
- source_rank.json

本文件仅定义结构冻结，不对代码、测试或配置做任何修改。

---

## 3. 数据结构冻结总览

| 文件名 | 语义 | 负责 Agent | 主要字段 | 冻结状态 |
| --- | --- | --- | --- | --- |
| search_results.json | 搜索发现结果 | NewsAgent | topic, status, search_keywords, search_results, facts, sources, statements, uncertainties, research_notes | 冻结 |
| news_articles.json | 新闻正文数据流 | NewsAgent | topic, status, articles, article_id, title, url, source, published_time, retrieved_time, content, summary, extraction_status | 冻结 |
| verification.json | 事实核验结果 | NewsVerifier | topic, article_id, source_id, articles, sources, facts, conflicts, uncertainties, verification_status, confidence | 冻结 |
| source_rank.json | 来源质量评级 | SourceRanker | source, type, level, score, count, risk, notes | 冻结 |

---

## 4. search_results.json 冻结结构

### 4.1 文件语义

search_results.json 为 NewsAgent 的搜索发现结果输出文件，用于保存检索阶段的发现与证据线索，不包含正式正文内容。

### 4.2 标准字段结构

```json
{
  "topic": "string",
  "status": "string",
  "search_keywords": ["string"],
  "search_results": [
    {
      "title": "string",
      "url": "string",
      "source": "string",
      "published_time": "string",
      "summary": "string"
    }
  ],
  "facts": ["string"],
  "sources": ["string"],
  "statements": ["string"],
  "uncertainties": ["string"],
  "research_notes": ["string"]
}
```

### 4.3 字段冻结规则

- `topic`：冻结为主题名称字段。
- `status`：冻结为状态字段，表示当前收集状态。
- `search_keywords`：冻结为关键词列表字段。
- `search_results`：冻结为搜索发现列表字段。
- `facts`：冻结为事实信息列表字段。
- `sources`：冻结为来源信息列表字段。
- `statements`：冻结为关键表述列表字段。
- `uncertainties`：冻结为不确定性列表字段。
- `research_notes`：冻结为研究备注字段。

### 4.4 结构约束

- search_results.json 仅保存“搜索发现结果”。
- 不得将搜索结果结构重命名为 `results`、`data`、`payload` 等非冻结名称。
- 不得将正文内容混入 search_results.json。
- 不允许在正式基线后将该文件替换为其他历史别名。

---

## 5. news_articles.json 冻结结构

### 5.1 文件语义

news_articles.json 为 NewsAgent 的新闻正文整理输出文件，用于保存抓取或整理后的正文内容与元数据，是 NewsVerifier 的正式输入源。

### 5.2 标准字段结构

```json
{
  "topic": "string",
  "status": "string",
  "articles": [
    {
      "article_id": "string",
      "title": "string",
      "url": "string",
      "source": "string",
      "published_time": "string",
      "retrieved_time": "string",
      "content": "string",
      "summary": "string",
      "extraction_status": "string"
    }
  ]
}
```

### 5.3 字段冻结规则

- `topic`：冻结为主题字段。
- `status`：冻结为状态字段。
- `articles`：冻结为正文主数组字段。
- `article_id`：冻结为正文唯一标识字段。
- `title`：冻结为文章标题字段。
- `url`：冻结为原文链接字段。
- `source`：冻结为来源字段。
- `published_time`：冻结为发布时间字段。
- `retrieved_time`：冻结为抓取/整理时间字段。
- `content`：冻结为正文内容字段。
- `summary`：冻结为摘要字段。
- `extraction_status`：冻结为抽取状态字段。

### 5.4 结构约束

- news_articles.json 仅保存“正文数据流”。
- 不允许用 `article_data`、`content_data`、`raw_text` 等非标准名称替代 `articles`。
- `articles` 数组中必须保留 `article_id` 与 `retrieved_time` 等关键字段。
- NewsVerifier 必须明确读取该文件，而非仅依赖搜索结果。

---

## 6. verification.json 冻结结构

### 6.1 文件语义

verification.json 为 NewsVerifier 的输出文件，用于保存核验过程中的事实与冲突分析结果。

### 6.2 标准字段结构

```json
{
  "topic": "string",
  "articles": [
    {
      "article_id": "string",
      "source_id": "string",
      "title": "string",
      "source": "string",
      "url": "string"
    }
  ],
  "sources": ["string"],
  "facts": ["string"],
  "conflicts": ["string"],
  "uncertainties": ["string"],
  "verification_status": "string",
  "confidence": 0.0
}
```

### 6.3 字段冻结规则

- `topic`：冻结为主题字段。
- `article_id`：冻结为 `articles` 数组内部文章唯一标识字段。
- `source_id`：冻结为 `articles` 数组内部来源唯一标识字段。
- `articles`：冻结为文章列表字段。
- `sources`：冻结为来源列表字段。
- `facts`：冻结为事实列表字段。
- `conflicts`：冻结为冲突列表字段。
- `uncertainties`：冻结为不确定性列表字段。
- `verification_status`：冻结为核验状态字段。
- `confidence`：冻结为置信度字段。

### 6.4 结构约束

- verification.json 不允许改名为 `review.json` 或其他历史别名。
- `article_id` 与 `source_id` 必须存在于 `articles` 对象内部，不允许重复定义在 verification.json 顶层。
- verification.json 不能被错误地等同于来源评级结果。
- 该文件必须作为 NewsVerifier 的正式输出结构冻结对象。

---

## 7. source_rank.json 冻结结构

### 7.1 文件语义

source_rank.json 为 SourceRanker 的输出文件，用于保存来源质量评级结果，不承担事实真伪判定职责。

### 7.2 标准字段结构

```json
{
  "source": "string",
  "type": "string",
  "level": "string",
  "score": 0,
  "count": 0,
  "risk": "string",
  "notes": "string"
}
```

### 7.3 字段冻结规则

- `source`：冻结为来源名称字段。
- `type`：冻结为来源类型字段。
- `level`：冻结为评级层级字段。
- `score`：冻结为评分字段。
- `count`：冻结为命中或出现次数字段。
- `risk`：冻结为风险说明字段。
- `notes`：冻结为备注字段。

### 7.4 结构约束

- source_rank.json 由 ProductionController 调度 SourceRanker 生成。
- SourceRanker 不作为 NewsVerifier 的直接强耦合下游组件。
- source_rank.json 仅表示来源质量评级结果，不参与事实真实性判断。
- 不得将其混淆为新闻真伪判定结果。
- 不得使用模糊命名替代 `source_rank.json`。
- 不允许将 `source_rank` 误理解为事实结果字段。

---

## 8. 字段命名冻结规则

### 8.1 通用规则

- `topic`：冻结为主题字段名。
- `status`：冻结为状态字段名。
- `source`：冻结为来源字段名。
- `source_id`：冻结为来源标识字段名。
- `article_id`：冻结为文章标识字段名。
- `retrieved_time`：冻结为抓取时间字段名。
- `content`：冻结为新闻正文内容字段。
- `summary`：冻结为新闻摘要字段。
- `confidence`：冻结为核验置信度字段。
- `extraction_status`：冻结为正文抽取状态字段。
- `published_time`：冻结为新闻发布时间字段。
- `verification_status`：冻结为核验状态字段名。
- `source_rank`：冻结为来源质量评级结果语义。

### 8.2 禁止事项

- 不得在正式基线后随意改名为 `results`、`data`、`payload` 等名称。
- 不得在不同文件间混用 `level`、`rank`、`category`、`type` 等语义不一致的字段。
- 不得在 `verification.json` 中使用 `review.json` 等历史别名。
- 不得将 `source_rank` 和事实真伪结论混为一谈。

---

## 9. 文件与层级冻结结论

当前 V2.0 数据结构冻结结论如下：

- search_results.json：冻结为 NewsAgent 的搜索发现结果文件，字段结构固定。
- news_articles.json：冻结为 NewsAgent 的新闻正文数据文件，字段结构固定。
- verification.json：冻结为 NewsVerifier 的核验结果文件，字段结构固定。
- source_rank.json：冻结为 SourceRanker 的来源评级文件，字段结构固定。

最终冻结原则：

- 文件名稳定
- 字段名稳定
- 对象层级稳定
- 语义边界稳定
- 上下游数据流不允许随意漂移
- 只有四个正式数据结构文件进入当前 V2.0 数据结构基线

本文件作为 V2.0 数据结构冻结基线文档，不直接修改代码、测试或配置。
