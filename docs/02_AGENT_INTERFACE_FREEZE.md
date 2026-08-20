# V2.0 Agent Interface Freeze

## 文档状态

V2.0 Agent Interface Freeze
Freeze Candidate Approved

---

## 1. Agent接口冻结目标

本文件基于已冻结的 Agent 基线 [docs/01_AGENT_BASELINE_FREEZE.md](docs/01_AGENT_BASELINE_FREEZE.md) 继续制定接口冻结方案，目标是：

1. 在当前 V2.0 基线中，明确四个正式 Agent 的输入、输出与调用边界。
2. 统一标准文件名、字段名、参数名，避免隐式依赖。
3. 禁止上游或下游自行扩展、重命名或修改接口定义。
4. 仅保留当前已实现的最小可运行接口集合，不扩展未落地 Agent。
5. 保证接口冻结后，Agent 之间可以通过标准文件和显式参数进行协作。

冻结范围：
- BaseAgent
- NewsAgent
- NewsVerifier
- SourceRanker

### 统一数据流

NewsAgent
↓
search_results.json
↓
news_articles.json
↓
NewsVerifier
↓
verification.json
↓
SourceRanker
↓
source_rank.json

---

## 2. BaseAgent 接口定义

| 项目 | 内容 |
| --- | --- |
| Agent名称 | BaseAgent |
| 输入 | 通用 Agent 输入对象，包含 Agent 名称、项目路径和业务输入 |
| 输入类型 | dict |
| 输入文件 | 无强制固定文件；仅允许显式参数对象或上下文对象 |
| 输出 | 通用执行结果对象、状态信息、错误信息 |
| 输出类型 | dict |
| 输出文件 | 无强制固定文件 |
| 调用方 | 所有 Agent |
| 被调用方 | 无固定下游，作为抽象基类存在 |

### BaseAgent 当前建议接口

输入：
- agent_name
- project_path
- input_data

输出：
- agent_name
- status
- result
- error

### BaseAgent 接口冻结规则

- BaseAgent 只允许统一基础行为，不允许各子类无约束重写接口语义。
- 任何子类不得依赖隐式全局变量读取上下文。
- 子类必须显式声明输入参数，不能通过隐藏状态修改上下游接口。

---

## 3. NewsAgent 接口定义

| 项目 | 内容 |
| --- | --- |
| Agent名称 | NewsAgent |
| 输入 | 新闻主题关键词 |
| 输入类型 | str 或 dict |
| 输入文件 | 允许无文件输入；若需要文件输入，必须显式传递 topic 或 project_path |
| 输出 | 搜索结果汇总对象 + 新闻正文整理对象 |
| 输出类型 | dict |
| 输出文件 | search_results.json, news_articles.json |
| 调用方 | 用户、ProductionController、上游任务入口 |
| 被调用方 | NewsVerifier |

### NewsAgent 当前建议接口

输入：
- topic_keyword

输出：
- search_results.json
- news_articles.json

建议字段：
- search_results.json：
  - topic
  - status
  - search_keywords
  - search_results
  - facts
  - sources
  - statements
  - uncertainties
  - research_notes
- news_articles.json：
  - topic
  - status
  - articles
  - article_id
  - title
  - url
  - source
  - published_time
  - retrieved_time
  - content
  - summary
  - extraction_status

### NewsAgent 关键接口约束

- 输入参数名称冻结为 topic 或 topic_keyword，且必须显式传入。
- 输出文件名称冻结为 search_results.json 与 news_articles.json。
- search_results.json 仅保存“搜索发现结果”。
- news_articles.json 仅保存“抓取或整理后的新闻正文信息”。
- NewsAgent 不能只输出 search_results.json，而忽略正文数据流。
- 不允许通过“隐式读取当前目录”方式寻找数据文件。
- 不允许在上游调用方未提供输入时，使用默认目录或默认内容进行自动补齐。

---

## 4. NewsVerifier 接口定义

| 项目 | 内容 |
| --- | --- |
| Agent名称 | NewsVerifier |
| 输入 | news_articles.json 或等价结构化对象 |
| 输入类型 | dict 或 JSON 文件路径 |
| 输入文件 | news_articles.json |
| 输出 | 验证结果对象 |
| 输出类型 | dict |
| 输出文件 | verification.json |
| 调用方 | NewsAgent、ProductionController |
| 被调用方 | SourceRanker |

### NewsVerifier 当前建议接口

输入：
- news_articles.json

输出：
- verification.json

建议字段：
- topic
- article_id
- source_id
- articles
- sources
- facts
- conflicts
- uncertainties
- verification_status
- confidence

### NewsVerifier 关键接口约束

- 输入应基于 news_articles.json，而不再只基于 search_results.json。
- NewsVerifier 必须显式接收正文输入对象或文件。
- 输出文件冻结为 verification.json。
- 不能自行将 verification.json 改成其他命名。
- 不得在下游接收时将 verification_path 作为隐式全局变量读取。
- 若输出 AI 辅助分析结果，也必须作为独立结构化对象，不破坏主输出契约。

---

## 5. SourceRanker 接口定义

| 项目 | 内容 |
| --- | --- |
| Agent名称 | SourceRanker |
| 输入 | verification.json 或来源清单 |
| 输入类型 | dict 或 JSON 文件路径 |
| 输入文件 | verification.json |
| 输出 | 来源质量评级结果 |
| 输出类型 | dict |
| 输出文件 | source_rank.json |
| 调用方 | ProductionController |
| 被调用方 | 后续扩展 Agent |

### SourceRanker 当前建议接口

输入：
- verification.json

输出：
- source_rank.json

建议字段：
- source
- type
- level
- score
- count
- risk
- notes

### SourceRanker 关键接口约束

- 输入文件名称冻结为 verification.json。
- 输出文件名称冻结为 source_rank.json。
- SourceRanker 只负责来源质量评级，不负责事实真实性判定。
- 不允许将 source_rank 直接等同于新闻真实性结果。
- 不允许使用模糊命名或历史别名替代正式接口名称。

---

## 6. 当前建议接口总览

| Agent | 输入 | 输入类型 | 输入文件 | 输出 | 输出类型 | 输出文件 | 调用方 | 被调用方 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BaseAgent | agent_name, project_path, input_data | dict | 无强制固定 | agent_name, status, result, error | dict | 无强制固定 | 所有 Agent | 无固定下游 |
| NewsAgent | topic_keyword | str / dict | 可选 | 搜索结果 + 新闻正文 | dict | search_results.json, news_articles.json | 用户、生产控制器 | NewsVerifier |
| NewsVerifier | news_articles.json | dict / path | news_articles.json | 验证结果 | dict | verification.json | NewsAgent、生产控制器 | SourceRanker |
| SourceRanker | verification.json | dict / path | verification.json | 来源质量结果 | dict | source_rank.json | ProductionController | 后续扩展 Agent |

---

## 7. 接口冻结规则

### 7.1 文件名称冻结

- search_results.json：冻结为 NewsAgent 搜索发现结果输出文件。
- news_articles.json：冻结为 NewsAgent 新闻正文整理输出文件。
- verification.json：冻结为 NewsVerifier 输出文件名称。
- source_rank.json：冻结为 SourceRanker 输出文件名称。
- 任何历史命名不应在正式基线中替代这些名称。

### 7.2 字段名称冻结

以下字段应优先保持稳定：

- topic
- source
- results
- status
- level
- score
- search_results
- news_articles
- articles
- article_id
- source_id
- retrieved_time
- verification_status
- source_rank

注意：
- 搜索结果结构中不允许在正式基线后随意改名为 results / data / payload 等不同命名。
- 新闻正文结构中不允许以 article_data / content_data / raw_text 等非标准名称替代 news_articles。
- verification.json 中不允许自行改成 review.json 或其他历史别名。
- verification.json 中必须保留 article_id 与 source_id。

### 7.3 参数名称冻结

- agent_name：冻结为 BaseAgent 的统一输入参数名称。
- project_path：仅作为项目路径参数，不应在不同 Agent 中混用为“文件路径/目录路径/单个文件路径”三种语义。
- input_data：冻结为 BaseAgent 的统一输入参数名称。
- verification_path：不得被用作隐式输入参数口径，必须显式指定验证文件。
- source_rank：不得被当作事实真伪判定字段，而应仅表示来源质量评级结果。
- topic_keyword：应作为标准输入参数名称，作为 NewsAgent 的标准入口。
- news_articles_path：应作为正文数据文件的显式入口参数名称，允许 NewsVerifier/后续流程显式读取正文数据。

### 7.4 不允许隐式依赖

- 不允许 Agent 通过 os.getcwd()、隐式当前目录、全局变量或全局缓存读取上下游文件。
- 每个 Agent 必须通过显式输入参数或显式文件路径获得依赖项。
- 不允许某个 Agent 依赖“某个文件必须在当前目录下”的隐含假设。
- NewsVerifier 不允许仅依赖标题搜索结果，而必须明确接收正文数据流。

### 7.5 不允许自行修改上下游接口

- NewsVerifier 不得自行修改 NewsAgent 的输入输出契约。
- SourceRanker 不得自行修改 NewsVerifier 的输出字段。
- BaseAgent 不得允许子类依赖不稳定的参数层级。
- 后续新增 Agent 必须在新版本中通过新增接口设计而不是破坏当前接口契约。

---

## 8. 当前发现的接口风险清单

### 8.1 project_path 风险

- project_path 在不同模块中可能被用于目录路径、项目根路径或单一文件路径。
- 这会导致上下游歧义，尤其在跨 Agent 调用时，容易出现“路径语义不一致”。
- 结论：project_path 必须在冻结后被统一为明确的项目级根路径参数，不允许用于单文件语义混用。

### 8.2 verification_path 风险

- verification_path 历史上可能被用于文件路径或对象引用。
- 若在不同 Agent 中被混用，会导致 NewsVerifier 与 SourceRanker 接口不一致。
- 结论：verification_path 仅允许作为显式输入文件路径，不得被替代为隐藏全局状态。

### 8.3 source_rank 风险

- source_rank 可能被错误理解为新闻真实性评级字段，而不是来源质量评级字段。
- 这会导致事实判定与来源评级混淆。
- 结论：source_rank 仅表示来源质量评级，不代表新闻“真假”结论。

### 8.4 search_results.json 风险

- search_results.json 可能在多个 Agent 中被替换成结果字典名称或不同文件名。
- 这会破坏 NewsVerifier 对输入的稳定读入契约。
- 结论：search_results.json 必须保持冻结名称，后续不得更改为 results.json 等别名。

### 8.5 news_articles.json 风险

- news_articles.json 是新增的正文数据流文件，必须从接口层明确区分于 search_results.json。
- 若后续仍只用 search_results.json，则会导致新闻正文数据缺失，无法支持核验、评级和热点分析。
- 结论：news_articles.json 必须被视为正式数据接口文件，且 NewsVerifier 的输入应优先基于它。

### 8.6 其他历史冲突

- results / search_results 双命名不统一
- source / name 语义不统一
- level / rank 语义不统一
- category / type 语义不统一
- verification_status / status 混用
- review.json / review_report.md 等命名混用

这些问题都需要在接口冻结阶段明确禁止继续扩散。

---

## 9. 接口冻结结论

当前 V2.0 接口冻结结论如下：

- BaseAgent：统一基础接口，不扩展隐式执行分支。
- NewsAgent：输入显式 topic_keyword，输出 search_results.json 和 news_articles.json。
- NewsVerifier：输入 news_articles.json，输出 verification.json。
- SourceRanker：由 ProductionController 编排调用，输入 verification.json，输出 source_rank.json。

最终冻结原则：

- 文件名稳定
- 字段名稳定
- 参数名稳定
- 上下游接口不可破坏
- 不允许隐式依赖
- 不允许跨 Agent 自行改名或扩展接口语义
- 新闻正文数据流必须被视为正式输出与输入的一部分。
- SourceRanker 由 ProductionController 调度，而非 NewsVerifier 的强耦合下游组件。

本文件仅作为接口冻结草案，不对任何代码或测试做修改。
