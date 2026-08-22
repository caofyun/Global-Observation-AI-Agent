《News Discovery V2.1 数据结构与接口设计》

版本：V2.1
阶段：设计冻结前审查稿
状态：设计阶段，不修改代码
适用项目：Global-Observation-AI-Agent

# 1. 设计目标

News Discovery V2.1 的目标不是替代现有 NewsAgent，也不是重新实现 Topic Pipeline V2.0。

它的核心任务只有一个：

根据用户给出的新闻需求，自动规划搜索方向，联网发现大量新闻候选，完成基础去重和标准化，并将候选新闻池交给已经通过测试的 Topic Pipeline V2.0。

因此，系统整体升级为：
用户新闻需求
      ↓
News Discovery V2.1
      ↓
自动生成搜索任务
      ↓
联网搜索
      ↓
原始新闻结果
      ↓
去重 / 标准化
      ↓
新闻候选池
      ↓
news_articles.json
      ↓
────────────────────────
Topic Pipeline V2.0
────────────────────────
      ↓
NewsVerifier
      ↓
SourceRanker
      ↓
TopicScorer
      ↓
TopicSelector
      ↓
动态 TOP N 选题
核心原则
保留 Topic Pipeline V2.0
不修改已经通过测试的 Agent
Discovery 独立于后续核验和评分
统一数据结构
topic 必须贯穿全链路
搜索结果与已核验新闻严格区分
没有真实正文时，content 必须为 null
不得用标题冒充正文
V2.1 先实现最小可用版本
后续再逐步增加 AI 搜索规划、全文抓取和语义聚类

# 2. News Discovery V2.1 在系统中的职责

News Discovery 不负责：

新闻事实核验
新闻来源可信度评级
热点评分
最终选题
脚本生成
视频制作

它只负责：
需求理解
   ↓
搜索任务规划
   ↓
联网搜索
   ↓
结果收集
   ↓
基础过滤
   ↓
去重
   ↓
标准化
   ↓
生成新闻候选池

因此职责边界为：
| 模块             | 职责   |
| -------------- | ---- |
| News Discovery | 发现新闻 |
| NewsVerifier   | 核验新闻 |
| SourceRanker   | 来源评级 |
| TopicScorer    | 热点评分 |
| TopicSelector  | 选题排序 |

# 3. News Discovery 输入接口

News Discovery V2.1 使用统一的 Discovery Request 作为输入接口。

Discovery Request 用于描述一次完整的新闻发现任务。

建议结构：

{
    "domain": "军事",
    "topic": "全球军事热点",
    "time_range": "24h",
    "geographic_scope": [
        "美国",
        "中东",
        "俄乌",
        "亚太"
    ],
    "focus_areas": [
        "航母",
        "军事部署",
        "军演",
        "导弹"
    ],
    "max_candidates": 100
}

其中：

- `domain` 表示长期关注领域。
- `topic` 表示本次 Discovery 任务的具体主题。
- `topic` 是整个 Topic Pipeline V2.0 的唯一主题标识。
- `domain` 可以为空，但 `topic` 不允许为空。

## 3.1 字段定义

| 字段 | 类型 | 必须 | 说明 |
|---|---|---:|---|
| `domain` | string/null | 否 | 新闻领域，例如军事、国际政治、经济 |
| `topic` | string | 是 | 本次新闻发现主题，也是全链路唯一主题标识 |
| `time_range` | string | 是 | 新闻发布时间范围 |
| `geographic_scope` | array | 否 | 地域范围 |
| `focus_areas` | array | 否 | 重点关注方向 |
| `max_candidates` | integer | 是 | 最终候选新闻数量上限 |

### 接口约束

1. `topic` 必须存在且不能为空。
2. `topic` 是本次 Discovery 任务的唯一主题来源。
3. Discovery 不得在缺少 `topic` 时自动生成 `"未知主题"`。
4. 如果 `topic` 缺失，Discovery Request 必须判定为无效请求并终止任务。
5. `domain` 用于描述长期新闻领域，不参与替代 `topic`。

## 3.2 topic

例如：
全球军事热点
或者：
中东局势
或者：

亚太军事动态

topic 是本次 Discovery 的全局主题标识。

后续整个 Pipeline 都必须继承该值。

## 3.3 time_range

第一版建议支持：

1h

6h

12h

24h

48h

7d

例如：

"time_range": "24h"

表示：

重点搜索最近24小时内发布的相关新闻。

### published_at 缺失时的时间过滤规则

V2.1 第一版中：

如果新闻的 published_at 有效，则必须按照 published_at 判断其是否属于 time_range。

如果 published_at = null，则无法确认该新闻是否属于指定时间范围。

因此：

published_at = null 的新闻不得作为满足 time_range 条件的候选新闻进入最终 articles。

Discovery 可以在内部保留该原始搜索结果用于统计，但不得将其写入最终 articles。

### 时间范围计算规则

V2.1 第一版的 `time_range` 统一按照新闻的 `published_at` 字段进行判断。

即：

```text
当前时间

    ↓

计算时间窗口

    ↓

检查 published_at

    ↓

判断新闻是否属于本次时间范围
```

## 3.4 geographic_scope

例如：
[
    "美国",
    "中东",
    "俄乌",
    "亚太"
]
为空时，可以由 Discovery 根据 topic 自行决定搜索范围。

## 3.5 focus_areas

例如：
[
    "航母",
    "军事部署",
    "军演",
    "导弹"
]

它用于扩大搜索覆盖面。

## 3.6 max_candidates

例如：
"max_candidates": 100

表示：

Discovery 最终最多向后续 Pipeline 输出100条候选新闻。

注意：

max_candidates 是候选池数量上限，不是搜索结果数量上限。

例如：
搜索结果：180条
        ↓
时间范围过滤
        ↓
基础有效性过滤
        ↓
URL 基础标准化与字符串去重
        ↓
标题基础标准化与字符串去重
        ↓
deduplicated_results
        ↓
max_candidates 限制
        ↓
最终写入 articles（最多100条）

其中，`max_candidates` 只限制最终写入 `articles` 的数量，
不限制 Search Query 数量、`raw_results` 或 `deduplicated_results`。

# 4. Search Query 数据结构

News Discovery 不应该只执行一个搜索词。

它需要首先生成多个搜索任务。

例如：
全球军事
美国军事
美国航母部署
美国军事行动
中东军事
伊朗军事
俄乌军事
俄罗斯军事部署
亚太军事
日本军事
朝鲜半岛军事
……

每一个搜索任务统一使用：
{
    "query": "美国航母最新部署",
    "category": "美国军事",
    "priority": 1,
    "query_index": 3
}

## 4.1 字段定义
| 字段            | 类型      | 必须 | 说明      |
| ------------- | ------- | -: | ------- |
| `query`       | string  |  是 | 实际搜索关键词 |
| `category`    | string  |  是 | 搜索方向    |
| `priority`    | integer |  是 | 搜索优先级   |
| `query_index` | integer |  是 | 查询序号    |

## 4.2 category

例如：
美国军事
中东军事
俄乌
亚太
军事装备
军事部署
军演
它不是最终新闻分类，而是：

这个 Query 为什么被搜索。

## 4.3 priority

建议：
1 = 高优先级
2 = 普通
3 = 扩展搜索
例如：
{
    "query": "美国航母最新部署",
    "category": "美国军事",
    "priority": 1,
    "query_index": 1
}



# 5. News Candidate 数据结构

Discovery 搜索之后，不直接把 SearchTool 原始数据交给后续 Pipeline。

先统一标准化为 News Candidate。

建议结构：

{
    "article_id": "ND-20260821-000001",
    "domain": "军事",
    "topic": "全球军事热点",
    "query": "美国航母最新部署",
    "queries": [
        "美国航母最新部署",
        "美国军事部署",
        "美国航母动态"
    ],
    "title": "……",
    "source": "Reuters",
    "url": "https://example.com/...",
    "published_at": "2026-08-21T15:30:00+09:00",
    "discovered_at": "2026-08-21T23:40:00+09:00",
    "summary": null,
    "content": null,
    "discovery_status": "DISCOVERED"
}

### query 与 queries 的区别

`query`：

表示本新闻被发现时的主搜索 Query。

`queries`：

表示本新闻被多个搜索 Query 命中时，记录所有产生匹配的 Query。

例如同一篇新闻同时被：

- 美国航母最新部署
- 美国军事部署
- 美国航母动态

三个 Query 搜索到，则：

"query": "美国航母最新部署"

同时：

"queries": [
    "美国航母最新部署",
    "美国军事部署",
    "美国航母动态"
]

### V2.1 最小实现要求

如果第一版实现暂时无法记录多个 Query：

`queries` 可以使用：

[
    "美国航母最新部署"
]

但字段结构必须保留。

### query 与 queries 的主 Query 规则

当一篇新闻仅被一个 Search Query 命中时：

`query` = 该 Search Query

`queries` = [该 Search Query]

当一篇新闻被多个 Search Query 命中时：

`queries` = 全部命中的 Search Query。

`query` = 其中 `priority` 最高的 Search Query。

如果多个 Query 的 `priority` 相同，则使用 `query_index` 最小的 Query 作为主 Query。

因此：

`query` 必须属于 `queries`。

即：

`query ∈ queries`

### 设计原则

一个新闻候选可以来自多个搜索 Query。

因此：

`query` 用于保持与现有代码和后续 Pipeline 的简单兼容。

`queries` 用于保存完整的 Discovery 来源信息。

# 6. News Candidate 字段定义

News Candidate 必须同时保存新闻本身的信息，以及 Discovery 发现该新闻时的基本来源信息。

| 字段 | 类型 | 必须 | V2.1 |
|---|---|---:|---|
| `article_id` | string | 是 | 必须 |
| `domain` | string/null | 否 | 可以为空 |
| `topic` | string | 是 | 必须 |
| `query` | string | 是 | 必须 |
| `queries` | array[string] | 是 | 必须 |
| `title` | string | 是 | 必须 |
| `source` | string | 是 | 必须 |
| `url` | string | 是 | 必须 |
| `published_at` | string/null | 否 | 可以为空 |
| `discovered_at` | string | 是 | 必须 |
| `summary` | string/null | 否 | 可以为空 |
| `content` | string/null | 否 | 必须允许为空 |
| `discovery_status` | string | 是 | 必须 |

其中：

`domain`

表示本次 Discovery 所属的长期新闻领域。

`topic`

表示本次 Discovery 的唯一主题标识。

`query`

表示该新闻被发现时的主搜索 Query。

`queries`

表示该新闻实际被哪些 Search Query 命中。

`query` 与 `queries` 必须保持语义一致。

`query` 用于保持与现有代码和后续 Pipeline 的简单兼容。

`queries` 用于保存完整的 Discovery 搜索来源信息。

第一版即使无法记录多个 Query，也必须保留 `queries` 字段，并至少保存当前主 Query。

# 7. content 的特殊规则

这是 V2.1 必须明确冻结的一条规则。

禁止：
"content": "美国航母最新部署"

如果这只是标题。

正确：
"content": null

因为当前 RSS 搜索结果没有真实正文。

因此：
SearchTool
    ↓
RSS
    ↓
title / source / url / published_time

不能假装已经取得正文。

# 8. summary 的规则

V2.1 第一阶段可以允许：
"summary": null

如果 RSS 没有可靠摘要。

也可以使用搜索源提供的真实 description/snippet。

但：

不能把 title 当 summary。

因此：
title
summary
content

三个字段必须保持语义独立。

# 9. discovery_status

建议 V2.1 使用：
DISCOVERED
作为正常状态。

异常情况可以使用：

SEARCH_RESULT
NORMALIZED
FAILED

但第一版不需要设计过多状态。

推荐最小状态集：

DISCOVERED
FAILED

其中：

DISCOVERED

表示：

已被 Discovery 发现并通过基础标准化。

它不代表：

新闻已经被核验。


# 10. news_articles.json 顶层结构

`news_articles.json` 是 News Discovery V2.1 与 Topic Pipeline V2.0 之间的标准文件接口。

V2.1 不再使用裸数组作为完整输出结构。

当前旧结构：

[
    {}
]

V2.1 统一使用对象结构：

{
    "schema_version": "2.1",
    "status": "SUCCESS",
    "domain": "军事",
    "topic": "全球军事热点",

    "discovery": {
        "time_range": "24h",
        "geographic_scope": [
            "美国",
            "中东",
            "俄乌",
            "亚太"
        ],
        "focus_areas": [
            "航母",
            "军事部署",
            "军演",
            "导弹"
        ],
        "discovered_at": "2026-08-21T23:40:00+09:00",

        "search_queries": [
            {
                "query": "美国军事最新动态",
                "category": "美国军事",
                "priority": 1,
                "query_index": 1
            },
            {
                "query": "美国航母最新部署",
                "category": "美国军事",
                "priority": 1,
                "query_index": 2
            }
        ],

        "query_count": 2
    },

    "statistics": {
        "raw_results": 120,
        "deduplicated_results": 83,
        "final_candidates": 83
    },

    "articles": [
        {
            "article_id": "ND-20260821-000001",
            "domain": "军事",
            "topic": "全球军事热点",
            "query": "美国航母最新部署",
            "queries": [
                "美国航母最新部署"
            ],
            "title": "……",
            "source": "Reuters",
            "url": "https://example.com/...",
            "published_at": "2026-08-21T15:30:00+09:00",
            "discovered_at": "2026-08-21T23:40:00+09:00",
            "summary": null,
            "content": null,
            "discovery_status": "DISCOVERED"
        }
    ]
}

## 10.1 顶层字段定义

| 字段 | 类型 | 必须 | 说明 |
|---|---|---:|---|
| `schema_version` | string | 是 | 数据结构版本 |
| `status` | string | 是 | 本次 Discovery 任务状态 |
| `domain` | string/null | 否 | 新闻领域 |
| `topic` | string | 是 | 本次 Discovery 唯一主题 |
| `discovery` | object | 是 | Discovery 元数据 |
| `statistics` | object | 是 | Discovery 统计数据 |
| `articles` | array | 是 | 新闻候选数组 |

## 10.2 status

V2.1 第一版建议使用：

`SUCCESS`

`FAILED`

其中：

`SUCCESS`：

表示 Discovery 任务已经正常完成。

SUCCESS 不代表一定发现了候选新闻。

如果本次 Discovery 正常执行，但没有发现符合条件的新闻，则：

`status = "SUCCESS"`

同时：

`articles = []`

表示 Discovery 正常完成，但本次没有发现符合条件的新闻候选。

`FAILED`：

表示 Discovery 任务本身无法正常完成，例如：

- Discovery Request 无效
- Search Query 无法生成
- 搜索任务整体失败
- 无法生成有效的 `news_articles.json`

`status` 描述的是 Discovery 任务状态。

它不表示新闻事实是否真实，也不表示来源是否可信。

`FAILED`：

表示 Discovery 任务失败，不能将该结果继续交给 Topic Pipeline。

`status` 描述的是 Discovery 任务状态。

它不表示新闻事实是否真实，也不表示来源是否可信。

## 10.3 topic

顶层 `topic` 是本次 Discovery 任务的唯一主题标识。

必须与 Discovery Request 中的：

`topic`

保持一致。

不得在 Discovery 输出阶段重新生成、修改或替换 topic。

不得使用：

"未知主题"

作为默认值。

## 10.4 discovery

`discovery` 用于记录本次新闻发现任务的搜索条件、搜索任务以及运行元数据。

至少包含：

- `time_range`
- `geographic_scope`
- `focus_areas`
- `discovered_at`
- `search_queries`
- `query_count`

其中：

`search_queries`

保存本次 Discovery 实际生成的全部 Search Query。

每一个 Search Query 必须符合第 4 节定义的数据结构：

- `query`
- `category`
- `priority`
- `query_index`

`query_count`

表示本次 Discovery 实际生成的 Search Query 数量。

后续版本可以增加：

- `search_engine`
- `search_duration`
- `failed_queries`

第一版暂不要求。

## 10.5 statistics

`statistics` 至少包含：

- `raw_results`
- `deduplicated_results`
- `final_candidates`

含义：

raw_results

所有 Search Query 返回的原始结果总数。

deduplicated_results

完成时间范围过滤、基础有效性过滤、URL 基础标准化与字符串去重、标题基础标准化与字符串去重后的新闻数量。

final_candidates

在 deduplicated_results 基础上执行 max_candidates 限制后，最终写入 articles 的新闻候选数量。

因此：

final_candidates <= deduplicated_results <= raw_results

## 10.6 articles

`articles` 是统一 News Candidate 数组。

每个元素必须符合第 6 节定义的 News Candidate 数据结构。

## 10.7 兼容性要求

V2.1 的 `news_articles.json` 必须保证后续 Topic Pipeline V2.0 能够读取：

`articles`

数组。

V2.1 可以增加顶层元数据，但不得改变：

`articles`

作为新闻候选数组的核心位置。

在正式实现前，需要通过现有 NewsVerifier 的实际代码确认其读取方式。

如果 NewsVerifier 当前读取：

`data["articles"]`

则 V2.1 结构可以直接兼容。

如果当前实现依赖其他结构，则应通过 Discovery Adapter 进行适配。

不得直接修改已经通过测试的 NewsVerifier。

# 11. 为什么要从裸数组升级为对象
当前：

[
    {},
    {}
]

无法直接表达：

这批新闻属于什么主题？
什么时候搜索的？
搜索了多少个 Query？
原始结果多少？
去重后多少？
最终多少？

而 V2.1：

{
    "schema_version": "2.1",
    "topic": "...",
    "discovery": {},
    "statistics": {},
    "articles": []
}

能够完整描述：

一次 Discovery 任务。

这也是后续自动化系统必须具备的能力。

# 12. discovery 元数据
建议：

"discovery": {
    "time_range": "24h",
    "geographic_scope": [],
    "focus_areas": [],
    "discovered_at": "...",
    "query_count": 12
}

后续可以增加：

search_engine
search_duration
failed_queries

但第一版不需要。

# 13. statistics

建议最少包含：

"statistics": {
    "raw_results": 120,
    "deduplicated_results": 83,
    "final_candidates": 83
}

含义：

raw_results

所有 Query 原始搜索结果总数。

`deduplicated_results`

经过时间范围过滤、基础有效性过滤、
URL 基础标准化与字符串去重、
标题基础标准化与字符串去重后的新闻数量。

final_candidates

在 `deduplicated_results` 基础上执行 `max_candidates` 限制后，
最终写入 `articles` 的数量。

# 14. Discovery Agent 输出接口
Discovery Agent 的最终输出不应该直接返回复杂 Python 对象给后续 Agent。

统一以：

news_articles.json

作为文件接口。

逻辑：

Discovery Request
       ↓
NewsDiscovery
       ↓
news_articles.json

输出至少包含：

schema_version
topic
discovery
statistics
articles

# 15. 与 Topic Pipeline V2.0 的连接

News Discovery V2.1 不直接修改 Topic Pipeline V2.0。

连接关系固定为：

News Discovery V2.1

        ↓

news_articles.json

        ↓

Discovery / Pipeline Adapter

        ↓

NewsVerifier

        ↓

verification.json

        ↓

SourceRanker

        ↓

source_rank.json

        ↓

TopicScorer

        ↓

topic_score.json

        ↓

TopicSelector

        ↓

topic_selection.json

这里必须坚持：

V2.1 只负责把新闻发现入口做好。

后面的 V2.0 Agent 不重新设计、不重构、不替换。

Adapter 只负责连接 V2.1 Discovery 与现有 V2.0 Pipeline，不承担新的新闻业务逻辑。

**### 15.1 Adapter 的职责**

Discovery / Pipeline Adapter 不是新的业务 Agent。

它只负责：

1. 读取 `news_articles.json`

2. 获取顶层 `topic`

3. 获取当前项目路径

4. 准备现有 V2.0 Agent 所需的调用参数

5. 按现有 V2.0 Agent 已支持的接口调用后续 Agent

6. 确保 topic 正确传递

7. 确保 Discovery 输出能够进入现有 Topic Pipeline

Adapter 不负责：

- 新闻搜索
- 搜索 Query 规划
- 新闻事实核验
- 来源评级
- 热点评分
- 选题排序

Adapter 的作用是：

V2.1 Discovery 输出

        ↓

接口适配 / 参数传递

        ↓

V2.0 Pipeline

因此 Adapter 不应成为新的业务处理层。

**### 15.2 Topic 传递规则**

`news_articles.json` 顶层：

"topic": "全球军事热点"

是本次 Discovery 任务的唯一 Topic Source of Truth。

调用 NewsVerifier 时，应将该 topic 通过其现有支持的参数传入。

例如：

NewsVerifier.run({

    "project_path": project_path,

    "topic_keyword": topic

})

这里的 `topic_keyword` 必须使用：

`news_articles.json` 中的 `topic`

而不是重新生成。

如果现有 NewsVerifier 的实际调用接口名称与上述示例不同，则 Adapter 必须按照现有代码实际支持的参数名称调用。

设计原则不变：

topic 必须来自：

`news_articles.json`

而不是由后续 Agent 重新推测。

**### 15.3 重要约束**

不得修改：

- NewsVerifier
- SourceRanker
- TopicScorer
- TopicSelector

如果现有 Agent 已经支持读取或接收 topic，则通过正确的调用参数完成主题传递。

如果现有 Agent 当前存在主题读取缺口，应优先通过 Adapter 或调用层解决。

只有在确认无法通过调用层解决时，才允许另行提出接口兼容性问题。

不得为了适配 Discovery 而重新设计已经通过测试的 V2.0 Agent。

V2.1 的目标是：

增加新的新闻发现入口，

而不是重新开发后续 Pipeline。

**### 15.4 完整 Topic 链路**

用户输入：

"全球军事热点"

↓

News Discovery Request

topic = "全球军事热点"

↓

News Discovery V2.1

↓

news_articles.json

topic = "全球军事热点"

↓

Discovery / Pipeline Adapter

topic = "全球军事热点"

↓

NewsVerifier

↓

verification.json

topic = "全球军事热点"

↓

SourceRanker

↓

source_rank.json

topic = "全球军事热点"

↓

TopicScorer

↓

topic_score.json

topic = "全球军事热点"

↓

TopicSelector

↓

topic_selection.json

topic = "全球军事热点"

整个链路必须识别并保持同一个 topic。

整个链路不得出现：

"未知主题"

**### 15.5 Topic Source of Truth**

本系统定义：

`Discovery Request.topic`

为本次 Discovery 与 Topic Pipeline 的唯一主题来源。

News Discovery 接收到的：

`Discovery Request.topic`

必须写入：

`news_articles.json.topic`

随后：

`news_articles.json.topic`

成为 Adapter 调用后续 Pipeline 时的 Topic Source of Truth。

任何后续 Agent 不得根据新闻标题重新推测、覆盖或生成新的 topic。

如果 topic 缺失：

Discovery Request

    ↓

请求无效

    ↓

Discovery 失败

而不是：

topic = "未知主题"

因此：

`"未知主题"`

不是合法的默认主题，也不是合法的数据补偿方式。

**### 15.6 Topic 传递原则**

V2.1 不要求修改现有 V2.0 Agent 来适应新的 Discovery。

如果现有 Agent 支持：

- `topic`
- `topic_keyword`
- 或其他已经存在的主题参数

则 Adapter 使用现有接口完成传递。

如果某个 V2.0 Agent 当前通过已有输入文件自然获得 topic，则继续使用现有机制。

如果某个 Agent 无法从现有调用方式获得正确 topic，则首先记录为接口兼容性问题，并通过 Adapter / Pipeline 调用层解决。

不得因为 Discovery V2.1 的加入而直接修改已经通过测试的 V2.0 Agent。

最终目标是：

Discovery Request.topic

        ↓

news_articles.json.topic

        ↓

Adapter

        ↓

verification.json.topic

        ↓

source_rank.json.topic

        ↓

topic_score.json.topic

        ↓

topic_selection.json.topic

确保整个 Pipeline 使用同一个 topic。

# 16. 与现有 NewsAgent 的关系
审计发现：

NewsAgent

目前已经具备：

搜索 Query 生成
多次调用 SearchTool
合并结果
基础去重

因此 V2.1 不应该把这些能力全部重新写一遍。

推荐：

News Discovery V2.1
       ↓
复用现有 SearchTool

而不是：

News Discovery
       ↓
重新开发新的搜索工具
# 17. NewsAgent 的定位

News Discovery V2.1 与现有 NewsAgent 的关系定义为：

NewsAgent 是现有搜索能力资产。

News Discovery V2.1 是新的上层新闻发现编排层。

V2.1 第一阶段不要求 News Discovery 必须调用 NewsAgent。

推荐正式架构为：

News Discovery
        ↓
Search Query
        ↓
SearchTool
        ↓
原始新闻结果
        ↓
去重 / 标准化
        ↓
news_articles.json

现有 NewsAgent 保留，不删除、不重构。

NewsAgent 当前已经具备：

- Search Query 生成
- 多次调用 SearchTool
- 合并结果
- 基础去重

这些能力属于现有项目资产。

V2.1 可以复用其中成熟的 SearchTool 和相关搜索逻辑，但不要求直接把 NewsAgent 作为 Discovery 的内部调用层。

这样可以避免：

News Discovery
        ↓
NewsAgent
        ↓
SearchTool

形成两层重复的 Query 规划和搜索编排。

V2.1 的职责边界冻结为：

News Discovery：

用户需求
↓
搜索策略
↓
Search Query
↓
SearchTool
↓
候选池

NewsAgent：

保留现有实现，作为现有项目搜索能力资产，不在 V2.1 第一阶段删除或重构。

后续如果确认 NewsAgent 的能力可以完整复用于 Discovery，可以再通过适配方式复用其成熟逻辑，但不影响 V2.1 的数据结构和接口设计。

# 18. 不建议第一版直接删除 NewsAgent
虽然 News Discovery 会逐渐承担 NewsAgent 的部分职责，但现在不要做：

删除 NewsAgent

或者：

重写 NewsAgent

因为：

当前 Topic Pipeline V2.0 已经 PASS。

稳定节点应该尽量保持稳定。

# 19. Discovery V2.1 最小实现方案
第一版只做以下事情：

① 接收 Discovery Request
        ↓
② 生成多个 Query
        ↓
③ 调用现有 SearchTool
        ↓
④ 合并原始结果
        ↓
⑤ 时间范围过滤
        ↓
⑥ 基础有效性过滤
        ↓
⑦ URL 基础标准化与字符串去重

### URL 去重规则

V2.1 第一版只进行基础 URL 标准化和字符串去重。

如果两个搜索结果经过相同的基础 URL 标准化规则处理后得到相同 URL，
则视为同一新闻候选。

V2.1 第一版暂不进行复杂的网页内容级 URL 解析，
也不进行语义级新闻去重。

复杂 URL 规范化和语义去重留待后续版本实现。
        ↓
⑧ 标题基础标准化与字符串去重
### 标题基础去重规则

V2.1 第一版允许进行基础标题字符串去重。

如果两个新闻候选经过基础标题标准化后得到相同标题，
则视为重复候选。

基础标题标准化仅用于消除明显的字符串差异，
不得进行语义级标题判断。

V2.1 第一版暂不判断两个不同标题是否属于同一新闻事件。

语义级新闻去重和事件聚类留待后续版本实现。

### 基础有效性过滤规则

V2.1 第一版的基础有效性过滤至少要求：

- `title` 非空
- `source` 非空
- `url` 非空且为有效 URL

如果缺少上述任一核心字段，则该搜索结果不得进入最终 `articles`。

以下字段允许为空：

- `domain`
- `published_at`
- `summary`
- `content`

其中：

`published_at = null` 的新闻无法满足第 3.3 节规定的时间范围条件，
不得进入最终 `articles`。
        ↓
⑨ 标准化字段
        ↓
⑩ 生成 article_id
        ↓
⑪ 执行 max_candidates 限制
        ↓
⑫ 写入 news_articles.json
        ↓
⑬ 交给 V2.0 Pipeline

其中，`max_candidates` 只限制最终写入 `articles` 的数量，
不限制 Search Query 数量、`raw_results` 或 `deduplicated_results`。

暂时不做：

AI 自动新闻摘要
正文抓取
LLM 语义去重
新闻聚类
新闻趋势分析
多轮自主搜索
搜索引擎自动切换



# 20. V2.1 第一版真正需要的搜索能力

假设：

topic = 全球军事热点

Discovery 可以根据：

- topic
- domain
- geographic_scope
- focus_areas
- time_range

生成多个 Search Query。

例如：

Query 1：美国军事最新动态

Query 2：美国航母最新部署

Query 3：美国军事行动

Query 4：中东军事最新动态

Query 5：伊朗军事最新消息

Query 6：以色列军事最新消息

Query 7：俄乌军事最新动态

Query 8：俄罗斯军事部署

Query 9：乌克兰战场最新消息

Query 10：亚太军事最新动态

Query 11：日本军事最新消息

Query 12：朝鲜半岛军事动态

上述 Query 数量仅为示例，不是 V2.1 的固定数量。

实际 Query 数量应由 Discovery 根据输入需求动态决定。

例如：

12 个 Query
×
每个 Query 最多 10 条结果
=
最多约 120 条原始结果

然后：

原始结果

↓

时间范围过滤

↓

基础有效性过滤

↓

URL 基础标准化与字符串去重

↓

标题基础标准化与字符串去重

↓

max_candidates 限制

↓

news_articles.json

因此：

V2.1 不再采用“预先设定5个选题，然后从5个选题中选择一个”的模式。

而是：

用户提出新闻需求

↓

Discovery 动态规划搜索方向

↓

互联网实时搜索

↓

几十～上百条新闻候选

↓

后续核验 / 来源评级 / 热点评分

↓

动态 TOP N

↓

用户最终选择

这才是 News Discovery V2.1 的核心价值。

# 21. 必须字段

Discovery Request：

- `topic`
- `time_range`
- `max_candidates`

其中：

`topic`

是全链路唯一主题标识，不能为空。

`time_range`

用于确定新闻时间范围，V2.1 第一版必须提供。

`max_candidates`

用于限制最终输出候选新闻数量。

可选字段：

- `domain`
- `geographic_scope`
- `focus_areas`

News Candidate：

- `article_id`
- `topic`
- `query`
- `queries`
- `title`
- `source`
- `url`
- `discovered_at`
- `discovery_status`

可以为空：

- `domain`
- `published_at`
- `summary`
- `content`

# 22. 可以暂时为空的字段
以下字段 V2.1 第一版允许为空：

published_at
summary
content

例如：

{
    "published_at": null,
    "summary": null,
    "content": null
}

这是合法状态。

# 23. 不允许伪造的数据
尤其禁止：

content = title

也禁止：

summary = title

除非搜索源本身确实提供了摘要，而且该摘要可以确认是摘要。

数据不足就：

null

而不是制造看起来完整的数据。

# 24. 后续升级路线
V2.1：

多 Query
+
搜索聚合
+
基础去重
+
标准化

↓

V2.2：

AI Query Planner

让 AI 根据用户需求自动设计搜索策略。

↓

V2.3：

正文抓取

获得真实新闻正文。

↓
V2.4：

语义去重 / 新闻事件聚类

例如：

20篇报道
     ↓
同一个事件
     ↓
Event Cluster

↓

V2.5：

多轮自主搜索

AI发现：

“美国航母部署”

然后自动进一步搜索：

部署地点
舰队规模
相关官方声明
其他媒体报道
历史背景

↓

最终：

News Discovery
       ↓
自主新闻研究
       ↓
事件聚类
       ↓
事实核验
       ↓
来源评级
       ↓
热点评分
       ↓
TOP 10

# 25. 最终架构

经过本次设计，推荐冻结为：

                    用户需求
                       │
                       ▼
             ┌──────────────────┐
             │ News Discovery   │
             │      V2.1        │
             └────────┬─────────┘
                      │
                 Search Query
                      │
                      ▼
                SearchTool
                      │
                      ▼
               原始新闻结果
                      │
                去重 / 标准化
                      │
                      ▼
              news_articles.json
                      │
                      ▼
          Discovery / Pipeline Adapter
                      │
══════════════════════╪══════════════════════
                      │
             Topic Pipeline V2.0
                      │
                      ▼
                NewsVerifier
                      │
                      ▼
                SourceRanker
                      │
                      ▼
                TopicScorer
                      │
                      ▼
                TopicSelector
                      │
                      ▼
                   TOP N
                      │
                      ▼
                  【用户选择】

其中：

News Discovery V2.1 负责新闻发现。

SearchTool 负责实际联网搜索。

Discovery / Pipeline Adapter 负责 V2.1 与 V2.0 之间的接口编排和参数传递。

Topic Pipeline V2.0 继续使用已经通过测试的：

NewsVerifier

SourceRanker

TopicScorer

TopicSelector

后续 V2.0 Agent 不因 V2.1 Discovery 的加入而重新设计。

# 26. 本阶段结论

News Discovery V2.1 的设计方向可以确认。
最重要的三个决定是：

第一

不推倒 V2.0。

现有：

NewsVerifier
SourceRanker
TopicScorer
TopicSelector

继续作为稳定核心。

第二

新增独立 Discovery 层。

News Discovery V2.1

负责解决：

“互联网每天到底有什么值得做的新闻？”

第三

从“固定选题评分”升级为“动态新闻发现”。

最终系统不是：

5个预设新闻
 ↓
选1个

而是：

互联网
 ↓
几十～上百条候选新闻
 ↓
核验
 ↓
来源评级
 ↓
热点评分
 ↓
TOP 10
 ↓
你选择

这才是真正符合你目标的AI 新闻选题工厂。