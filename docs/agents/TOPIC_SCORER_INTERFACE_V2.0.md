# TopicScorer V2.0 接口规范

版本：TopicScorer V2.0

状态：设计冻结

# TopicScorer V2.0 接口规范


| 项目 | 内容 |
|-|-|
| Agent名称 | TopicScorer |
| 版本 | V2.0 |
| 状态 | 设计冻结 |
| 输入 | source_rank.json |
| 输出 | topic_score.json |
| 上游Agent | SourceRanker |
| 下游Agent | ScriptAgent |


---

## 设计目标

本文档定义 TopicScorer V2.0 的：

- 输入接口
- 输出接口
- 数据结构
- 评分模型
- 推荐规则
- Agent职责边界


禁止：

- 修改 BaseAgent
- 修改 NewsAgent
- 修改 NewsVerifier
- 修改 SourceRanker

**TopicScorer V2.0 接口规范**

**总体说明**
- **继承关系**：`TopicScorer` 应继承 `BaseAgent` 并遵循 `BaseAgent` 的 `run(input_data)` / `execute(input_data)` 约定，保持与现有 Agent 接口完全兼容（不修改已有 Agent）。
- **目的**：根据上游核验与来源评级结果，评估新闻主题是否值得进一步制作（如制作视频），产出结构化的 `topic_score.json` 供下游 `ScriptAgent` 使用。

**Agent 名称**
- `TopicScorer`

**Agent 职责**
- 读取上游产物（至少为 `source_rank.json`），结合 `verification.json` / `news_articles.json`（可选）计算热点价值与制作建议。
- 输出标准化的评分文件 `topic_score.json` 并写入项目目录（详见输出文件）。
- 不负责修改上游文件或下游执行，仅负责评分决策输出。

**输入文件（优先级）**
- 核心输入（必须）：`<project_path>/03_来源评级/source_rank.json`（由 `SourceRanker` 生成）
- 辅助输入（建议）：`<project_path>/02_事实核验/verification.json`（由 `NewsVerifier` 生成；用于时间、事实与文章级别细节）
- 禁止直接依赖（架构约束）：`<project_path>/01_新闻资料/search_results.json` — Agent 间通过标准 JSON 通信，不跨层读取原始上游搜索输入。
- 备用（可选）：`<project_path>/01_新闻资料/news_articles.json`（仅在确需原始正文或更细粒度发布时间分布时使用，且应优先通过 `NewsVerifier` 输出的 `verification.json` 获取信息）

**输出文件**
- 主输出：`<project_path>/04_热点评分/topic_score.json`
- 文件应可被 `ScriptAgent` 直接读取以生成脚本（见下文的对接说明）。

**输入 JSON 结构 说明（示例片段）**
- `source_rank.json`（约定字段）：
  {
    "topic": "...",
    "sources": [
      {
        "source_id": "source_1",
        "source_name": "BBC",
        "source_type": "媒体/官方/博客",
        "credibility_score": 90,
        "verification_score": 70,
        "source_rank": "A",
        "reason": "..."
      },
      ...
    ]
  }
- `verification.json`（约定字段片段）：
  {
    "topic": "...",
    "articles": [ { "article_id":"article_1", "published_time":"2026-08-14T22:25:00Z", "source":"BBC", "summary":"..." }, ... ],
    "sources": ["BBC","RFI",...],
    "verification_status": "MULTIPLE_SOURCES_FOUND",
    "confidence": "HIGH"
  }

**输出 `topic_score.json` 结构规范**
- 主体结构（字段类型说明）：
  {
    "topic": "string",                      // 主题名称
    "score": 0-100 (number),                 // 总分（整数或小数，建议取整）
    "recommendation": "制作|观望|不制作",  // 建议
    "breakdown": {
      "international_influence": 0-100,
      "news_hotness": 0-100,
      "user_interest": 0-100,
      "video_potential": 0-100,
      "source_quality": 0-100
    },
    "weights": {                             // 最终使用的权重（可在运行日志/元数据中保留）
      "international_influence": 0.25,
      "news_hotness": 0.30,
      "user_interest": 0.20,
      "video_potential": 0.15,
      "source_quality": 0.10
    },
    "meta": {
      "unique_source_count": int,
      "earliest_published": "ISO8601|string|null",
      "latest_published": "ISO8601|string|null",
      "top_sources": ["BBC","新华社"],
      "generated_at": "ISO8601 timestamp",
      "version": "TopicScorer v2.0"
    }
  }

**评分维度（定义与计算要点）**
- `international_influence`（国际影响力）：衡量报道涉及的国家/地区范围、国际媒体报道覆盖度、是否涉及国际组织或高层决策。可由 `sources` 中跨国家媒体数量、顶级媒体占比等启发式指标计算。
- `news_hotness`（新闻热度）：衡量短期内报道密度与时间分布（例如过去72小时内文章数、发布时间集中程度、发布时间窗口内增长率）。
- `user_interest`（用户关注度）：若有外部信号（搜索量、社媒互动）则为主；

  注：V2.0 阶段 `user_interest` 应使用代理指标（proxy），**不得直接接入外部平台数据**。常见代理来源包括标题/摘要关键词命中热点词库、上游 `NewsVerifier`/`SourceRanker` 的相对排名或文章密度。V3.0 可扩展为接入 `user_signal.json` 等外部用户交互数据源以提高精度。
- `video_potential`（视频传播潜力）：评估内容是否适合视频呈现（视觉要素、故事性、明确钩子）。可通过关键词匹配（冲突、人物、画面感词）和摘要长度/事实点数估算。
- `source_quality`（来源质量）：由 `source_rank.json` 中各来源 `credibility_score` 与 `verification_score` 的加权聚合得到，反映信息可靠性与权威性。

**评分公式（建议）**
- 每个维度先计算或估算为 0-100 的子分值 s_i。
- 使用权重 w_i 对子分值进行加权平均计算总体得分：

  final_score = round( (Σ w_i * s_i) / (Σ w_i) )

  其中默认权重见上文 `weights`。

- 子分值计算示例（说明，不是具体硬编码）：
  - `source_quality` = normalized( mean(credibility_score, verification_score) )
  - `news_hotness` = normalized( f(articles_count_last_72h, time_decay_factor, unique_source_count) )
  - `international_influence` = normalized( number_of_countries_covered * top_media_ratio )
  - `user_interest` = normalized( external_signals OR keyword_hotness_proxy )
  - `video_potential` = normalized( visual_keyword_score + narrative_points )

  说明：normalized 表示将指标映射到 0-100 的线性或分段函数，需在实现阶段确定映射细节与阈值。

**权重设计（建议默认值，后续可调整）**
- 推荐初始权重（可在配置中覆盖，但默认值应固定）：
  - `international_influence`: 0.25
  - `news_hotness`: 0.30
  - `user_interest`: 0.20
  - `video_potential`: 0.15
  - `source_quality`: 0.10

  说明：热度与国际影响优先考虑，为主导决策维度；来源质量作为可信度补充权重较低，但在 `confidence` 低或 `verification_status` 异常时应影响最终推荐（见推荐规则）。

**recommendation 规则（阈值示例）**
- 基于 `score` 产生三档推荐：
  - `制作`：score >= 80，且 `source_quality` >= 50 或 `verification_status` 为 MULTIPLE_SOURCES_FOUND
  - `观望`：60 <= score < 80，或 score >= 80 但 `source_quality` < 50（需要人工复核）
  - `不制作`：score < 60，或 `verification_status` 为 NO_VALID_SOURCE 且 `source_quality` 低

  说明：当 AI/上游置信度（`verification.json` 中 `confidence`）为 LOW，或存在大量 `uncertainties`/`conflicts` 时，`TopicScorer` 应降低最终推荐等级或标注 `human_review_required`（可在 `meta` 中扩展标注字段）。

**与后续 `ScriptAgent` 的数据接口（契约）**
- `ScriptAgent` 期望接收来自 `TopicScorer` 的 `topic_score.json`，并至少使用下列字段：
  - `topic`：主题文本
  - `recommendation`：制作建议（用以判断是否进入脚本生产）
  - `score`：总体分数（用于排序/优先级队列）
  - `breakdown`：各维度分值（可用于脚本风格/侧重点选择，例如高 `video_potential` 倾向视觉化脚本）
  - `meta.top_sources`：用于在脚本中引用权威来源

- 接口契约要求：`topic_score.json` 必须可被 `ScriptAgent` 直接读取解析，字段命名与类型必须一致，除 `meta` 外不应使用实现内部额外未记录字段来传递关键信息。

**错误处理与兼容性**
- 若缺少 `source_rank.json`，`TopicScorer` 应返回错误并不生成 `topic_score.json`（遵循现有 Agent 的错误抛出/返回风格）。
- 若 `verification.json` 缺失，TopicScorer 应在 `meta` 中记录缺失信息并尽量使用 `source_rank.json` 可用字段完成评分。
- 不得修改已冻结 Agent 的输出格式；仅通过读取其产物进行评分。

**可扩展项（建议记录在实现后续规范中）**
- 支持外部用户兴趣信号的采集接口（例如 `user_signal.json`）以增强 `user_interest` 指标。
- 若后续拆分 HotspotScore，可将 `news_hotness` 的计算逻辑抽出为单独 Agent（HotspotScorer），由 TopicScorer 调用或消费其输出。

**示例：最小可行输出（示例 JSON）**
{
  "topic": "美国航母部署动态",
  "score": 82,
  "recommendation": "制作",
  "breakdown": {
    "international_influence": 85,
    "news_hotness": 90,
    "user_interest": 70,
    "video_potential": 80,
    "source_quality": 60
  },
  "weights": {
    "international_influence": 0.25,
    "news_hotness": 0.30,
    "user_interest": 0.20,
    "video_potential": 0.15,
    "source_quality": 0.10
  },
  "meta": {
    "unique_source_count": 20,
    "earliest_published": "2026-08-14T22:25:00Z",
    "latest_published": "2026-08-20T06:37:12Z",
    "top_sources": ["BBC","新华社","DW.com"],
    "generated_at": "2026-08-21T12:00:00Z",
    "version": "TopicScorer v2.0"
  }
}

---
备注：本文件仅为设计规范，遵循项目 V2.0 架构与冻结约束（不修改 `BaseAgent`、`NewsAgent`、`NewsVerifier`、`SourceRanker`，不变更已有接口）。实现阶段应基于本规范进一步细化子分值的归一化函数、时间窗口定义与外部信号接入方案。
