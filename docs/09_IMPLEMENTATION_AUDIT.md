# V2.0 Implementation Audit

## 文档状态

V2.0 Implementation Audit
Freeze Approved

---

## 1. 审计目标

本文件基于已冻结的 V2.0 架构与实施文档：

- [docs/01_AGENT_BASELINE_FREEZE.md](01_AGENT_BASELINE_FREEZE.md)
- [docs/02_AGENT_INTERFACE_FREEZE.md](02_AGENT_INTERFACE_FREEZE.md)
- [docs/03_DATA_STRUCTURE_FREEZE.md](03_DATA_STRUCTURE_FREEZE.md)
- [docs/04_PRODUCTION_WORKFLOW_FREEZE.md](04_PRODUCTION_WORKFLOW_FREEZE.md)
- [docs/05_IMPLEMENTATION_ROADMAP_FREEZE.md](05_IMPLEMENTATION_ROADMAP_FREEZE.md)

进行 V2.0 Implementation Audit，目的仅为：

1. 检查当前代码与已冻结架构的差异。
2. 验证 BaseAgent、NewsAgent、NewsVerifier、SourceRanker、ProductionController 是否符合已冻结协议。
3. 核对标准文件流是否一致：search_results.json、news_articles.json、verification.json、source_rank.json。
4. 识别历史接口、旧字段、隐式依赖和流程偏差。
5. 不修改代码、不重构架构、不扩展未来功能，仅保留审计结论。

---

## 2. 审计范围

本次审计聚焦当前代码与冻结文档的以下一致性：

- BaseAgent 接口契约
- NewsAgent 输出协议
- NewsVerifier 输入输出协议
- SourceRanker 输入输出协议
- ProductionController 流程职责
- 标准文件命名和路径边界
- 历史接口、旧字段、隐式依赖检查

审计原则：

- 不新增 Agent
- 不重新设计架构
- 不修改冻结数据结构
- 不提出未来功能扩展
- 只检查“代码现状”和“冻结标准”之间的差距

---

## 3. 当前代码与冻结标准差异列表

### 3.1 BaseAgent 接口契约差异

冻结要求：

- BaseAgent 统一基础接口语义
- 输入应包含：agent_name、project_path、input_data
- 输出应包含：agent_name、status、result、error

当前代码差异：

- [src/agents/base_agent.py](../src/agents/base_agent.py) 中 BaseAgent 的返回字段为 `name`、`status`、`result`、`error`。
- 冻结标准强调统一接口语义和字段命名稳定性；当前字段名称 `name` 与冻结字段 `agent_name` 不一致。
- 运行状态目前为 `COMPLETED` / `ERROR`，而冻结文档要求以统一标准语义为主线，且应在后续实施阶段与统一状态机保持一致。

风险：

- 接口不统一，调用方需要额外适配。
- 后续代码与文档语义偏离，易出现隐式接口依赖。

---

### 3.2 NewsAgent 输出协议差异

冻结要求：

- NewsAgent 输入：topic_keyword
- 输出：search_results.json、news_articles.json
- news_articles.json 是正式正文数据流，必须与 NewsVerifier 对接

当前代码差异：

- [src/agents/news_agent.py](../src/agents/news_agent.py) 目前生成的是 `search_results.json`，但未见符合冻结要求的 `news_articles.json` 正文文件输出。
- 当前逻辑主要聚焦搜索结果收集与去重，未显式形成正文结构数据流。
- 与冻结的新闻正文数据流要求不一致，导致下游 NewsVerifier 无法按标准输入读取。

风险：

- NewsVerifier 无法按冻结要求从 news_articles.json 读取正文流。
- 关键数据链路被中断，流程无法真正确认标准文件流。

---

### 3.3 NewsVerifier 输入输出协议差异

冻结要求：

- NewsVerifier 输入：news_articles.json
- 输出：verification.json
- verification.json 结构必须符合冻结字段约束

当前代码差异：

- [src/agents/news_verifier.py](../src/agents/news_verifier.py) 中 `execute()` 目前读取的是 `search_results.json`。
- 代码中 `search_results_path` 逻辑仍为历史接口模式。
- 生成的结构中包含 `status`、`total_search_results`、`valid_results`、`source_counts`、`results`、`invalid_results` 等字段，不符合冻结文档中的 `topic`、`articles`、`sources`、`facts`、`conflicts`、`uncertainties`、`verification_status`、`confidence` 结构。
- 代码中额外生成 `ai_verification.json`，属于非冻结输出。

风险：

- 数据流不符合正式 V2.0 生产链路。
- 下游 SourceRanker 无法从冻结标准结构获取来源评级信息。

---

### 3.4 SourceRanker 输入输出协议差异

冻结要求：

- SourceRanker 输入：verification.json
- 读取来源相关结构进行评级
- 输出：source_rank.json
- 只负责来源质量评级，不承担事实判断职责

当前代码差异：

- [src/agents/source_ranker.py](../src/agents/source_ranker.py) 中 `execute()` 读取的是 `verification_path`，属于历史接口参数扩散。
- 代码读取 `data.get("results")`，并对其进行来源汇总；这属于旧的任务结构模型，不符合冻结要求。
- 输出结构包含 `topic`、`total_sources`、`unique_sources`、`quality_score`、`quality_level`、`sources`、`warnings` 等字段，偏离冻结文档的 `source`、`type`、`level`、`score`、`count`、`risk`、`notes` 结构。
- 代码没有明显表现出“只负责来源评级”的边界清晰性，历史结构仍偏强于结果聚合。

风险：

- SourceRanker 与 NewsVerifier 的职责边界模糊。
- 评级结果不满足正式裁剪标准。

---

### 3.5 ProductionController 流程职责差异

冻结要求：

- ProductionController 仅负责流程编排与状态管理
- 正式链路：NewsAgent → NewsVerifier → SourceRanker
- 不承担专业业务判断逻辑

当前代码差异：

- [src/core/production_controller.py](../src/core/production_controller.py) 当前仅创建项目并打印状态，未体现冻结中的完整调度链。
- 代码中 `下一阶段：新闻分析` 等信息表明它仍停留在早期项目脚手架状态，而不是标准 V2.0 生产编排。
- 该类未实现以标准任务顺序管控 Agent 执行，且未执行基于文件依赖的流程校验。

风险：

- 仍然不是正式 V2.0 编排层。
- 无法保证标准任务顺序和文件依赖链的稳定执行。

---

### 3.6 文件命名与数据流差异

冻结要求：

- 文件链路定义为：search_results.json → news_articles.json → verification.json → source_rank.json
- 文件命名必须保持稳定，且遵从标准约束

当前代码差异：

- [src/agents/news_agent.py](../src/agents/news_agent.py) 仅输出 search_results.json。
- [src/agents/news_verifier.py](../src/agents/news_verifier.py) 从 search_results.json 读取并输出 verification.json。
- [src/agents/source_ranker.py](../src/agents/source_ranker.py) 读取 verification_path，生成 source_rank.json。
- [src/agents/news_verifier.py](../src/agents/news_verifier.py) 额外输出 ai_verification.json，超出冻结范围。

结论：

- 当前文件链路不符合冻结要求。
- 标准流未真正落地。

---

### 3.7 历史接口、旧字段与隐式依赖差异

冻结要求：

- 不依赖隐式全局状态
- 不允许使用历史别名/旧字段替代正式接口
- 不允许产生 `xxx_path` 之类的接口扩散

当前代码差异：

- [src/agents/news_verifier.py](../src/agents/news_verifier.py) 中存在 `search_results_path`、`project_path` 组合方式。
- [src/agents/source_ranker.py](../src/agents/source_ranker.py) 中存在 `verification_path`，并要求 `verification_path` 为显式参数。
- 代码中多个地方依赖自动搜索目录和默认文件路径，属于隐式依赖风险。
- 这类接口和字段模式与冻结要求中的统一项目上下文 `project_path` 以及标准文件流存在冲突。

风险：

- 接口漂移和字段混用。
- 后续实现中可能出现大量历史命名残留。

---

## 4. P0 / P1 / P2 问题分类

### P0（最高优先级）

1. NewsAgent 未按冻结规则产出 news_articles.json
2. NewsVerifier 仍按旧 search_results 流读取，而非 news_articles.json
3. verification.json 结构与冻结标准不一致
4. 关键路径仍不满足正式 V2.0 文件流要求

### P1（高优先级）

1. BaseAgent 接口字段不符合冻结要求
2. SourceRanker 读取/输出结构不符合正式契约
3. ProductionController 未实现正式调度职责
4. ai_verification.json 属于非冻结扩展输出

### P2（中优先级）

1. 隐式路径与默认目录依赖仍存在
2. `search_results_path` / `verification_path` 等历史参数扩散
3. 代码中仍有历史接口模型残留，容易阻碍正式冻结协议落地

---

## 5. 核心差距总结

当前代码的核心差距，可以概括为以下几点：

- 代码实现仍然保留历史“搜索结果主导”的数据模型，而非冻结后的“正文数据流主导”的模型。
- Agent 对接口语义的约束不够严谨，仍存在字段名和参数名不统一的情况。
- NewsVerifier 和 SourceRanker 的职责边界没有完全对齐冻结要求。
- ProductionController 尚未成为真正的流程编排层。
- 标准文件流没有真正落地，尤其缺少 `news_articles.json` 正文流的正式实现。

换言之，当前代码更接近“早期原型状态”，而不是“已冻结 V2.0 正式实现状态”。

---

## 6. 修复优先级建议

### 优先级 1：接口与文件流收口

- 修正 BaseAgent 接口契约
- 统一 `project_path` 作为项目上下文
- 修正 NewsAgent 与 NewsVerifier 的数据流边界
- 确保 `news_articles.json` 成为正式正文数据流

### 优先级 2：标准输出结构修正

- 修正 `verification.json` 结构
- 修正 `source_rank.json` 结构
- 删除非冻结输出 `ai_verification.json`

### 优先级 3：流程编排修正

- 让 ProductionController 只负责流程调度、状态管理、文件依赖检查
- 恢复标准顺序：NewsAgent → NewsVerifier → SourceRanker

### 优先级 4：历史接口清理

- 消除 `search_results_path`、`verification_path` 等扩散参数
- 处理默认目录与隐式搜索行为
- 统一文件依赖表达方式

---

## 7. 审计结论

当前项目尚未达到 V2.0 冻结文档要求的实现一致性。

审计结论如下：

- BaseAgent 接口：部分符合基础结构，但仍存在字段语义差异。
- NewsAgent：未完整符合冻结的输出协议。
- NewsVerifier：关键输入输出链路仍偏离冻结要求。
- SourceRanker：输入输出和职责边界仍需收口。
- ProductionController：未达到正式编排层要求。
- 文件流：当前未形成标准化的 `search_results.json → news_articles.json → verification.json → source_rank.json` 流程。

因此，本次审计结论为：

V2.0 Implementation Audit：未通过

仅保留审计结果，不修改代码、不扩展功能、不重构架构。 
