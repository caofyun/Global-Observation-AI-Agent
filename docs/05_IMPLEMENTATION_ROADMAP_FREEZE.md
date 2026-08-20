# V2.0 Implementation Roadmap Freeze

## 文档状态

V2.0 Implementation Roadmap Freeze
Freeze Approved

---

## 1. Roadmap Freeze目标

本文件基于已冻结的 V2.0 架构文档：

- [docs/01_AGENT_BASELINE_FREEZE.md](01_AGENT_BASELINE_FREEZE.md)
- [docs/02_AGENT_INTERFACE_FREEZE.md](02_AGENT_INTERFACE_FREEZE.md)
- [docs/03_DATA_STRUCTURE_FREEZE.md](03_DATA_STRUCTURE_FREEZE.md)
- [docs/04_PRODUCTION_WORKFLOW_FREEZE.md](04_PRODUCTION_WORKFLOW_FREEZE.md)

在当前 V2.0 正式基线内，冻结“仅针对现有代码适配”的实施路线图，目标是：

1. 明确当前代码需要修正的差距范围，不扩展未落地功能。
2. 统一 BaseAgent、NewsAgent、NewsVerifier、SourceRanker 与 ProductionController 的实现边界。
3. 让现有代码逐步适配冻结的 Agent 名称、接口、文件结构和执行顺序。
4. 保持数据结构冻结不变，不新增 Agent，不新增未来模块。
5. 重点解决“当前代码与冻结架构不一致”问题，而不是设计新能力。

---

## 2. 冻结范围

本次 Implementation Roadmap Freeze 仅覆盖当前已有代码的适配工作，范围包括：

- BaseAgent 统一接口修正
- NewsAgent 对 topic_keyword、搜索与正文输出的适配
- NewsVerifier 对 news_articles.json 的读取与 verification.json 输出的适配
- SourceRanker 对 verification.json 中来源信息的读取与 source_rank.json 输出的适配
- ProductionController 的流程调度、状态管理与文件依赖校验适配

冻结边界：

- 不新增 Agent
- 不新增未来功能模块
- 不扩展视频/音频/素材等后续生产链路
- 不修改冻结的数据结构
- 不允许在当前 V2.0 正式基线中引入未冻结的设计扩展

---

## 3. 当前代码与冻结架构差距的重点问题

### 3.1 Agent 命名与职责差距

当前代码应以已冻结基线为准：

- BaseAgent
- NewsAgent
- NewsVerifier
- SourceRanker

禁止使用未冻结的历史命名或候选名称替代正式 Agent 名称。所有实现层面必须保证：

- 代码类名与文档命名保持一致
- 角色职责与冻结职责一致
- 未冻结 Agent 不能被混入正式流程

### 3.2 接口语义差距

当前实现需优先对齐以下接口契约：

- BaseAgent 输入：agent_name、project_path、input_data
- BaseAgent 输出：agent_name、status、result、error
- NewsAgent 输入：topic_keyword
- NewsAgent 输出：search_results.json、news_articles.json
- NewsVerifier 输入：news_articles.json
- NewsVerifier 输出：verification.json
- SourceRanker 输入：verification.json 读取 sources 字段用于来源质量评级
- SourceRanker 输出：source_rank.json

重点要求：

- 明确参数传递，不依赖隐式全局状态
- 明确文件输入输出，不允许绕过标准数据流
- 不允许在接口层使用历史别名或隐式目录依赖

> 实施阶段注意：当前冻结文档已统一方向，但代码实现时仍需明确项目上下文统一使用 `project_path`，避免出现 `verification_path`、`news_path`、`xxx_path` 等接口扩散。正式基线中建议保留 `project_path` 作为统一项目上下文，不对每个 Agent 额外生成不同的路径参数。

> 实施阶段注意：SourceRanker 的来源评级输入不应被写死为 `verification["sources"]` 固定结构。未来代码实现时，应允许读取 `verification.get("sources")`，以及来源相关结构的兼容表达，例如 `sources: ["Reuters"]` 或 `sources: [{"source":"Reuters","source_id":"001"}]`；核心是读取来源相关信息进行评级，而不是硬编码单一结构。

### 3.3 数据结构差距

当前实现必须遵循已冻结的四类标准文件结构：

- search_results.json：搜索发现结果
- news_articles.json：正文数据流
- verification.json：事实核验结果
- source_rank.json：来源质量评级结果

不得修改以下冻结结构语义：

- topic
- status
- articles
- article_id
- source_id
- confidence
- verification_status
- source
- score
- risk
- notes

### 3.4 流程编排差距

当前代码必须对齐正式链路：

ProductionController

↓

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

要求：

- 生产链路唯一且固定
- Agent 之间不直接绕过控制器调用
- ProductionController 仅承担编排与状态记录，不承担专业业务逻辑
- 关键文件缺失必须触发流程终止

---

## 4. 实施路线图冻结

### Phase 1：Agent 接口对齐

目标：让当前代码符合已冻结的 BaseAgent 与子 Agent 契约。

实施内容：

- 确认 BaseAgent 基础接口语义统一
- 统一各 Agent 的执行返回结构：agent_name、status、result、error
- 修正不一致的调用参数和返回字段名
- 统一错误处理入口与状态输出

交付要求：

- 所有 Agent 具备统一返回对象
- 失败状态可追踪
- 无隐藏状态依赖

### Phase 2：文件输入输出对齐

目标：确保当前代码输出和读取的文件满足冻结文件边界。

实施内容：

- NewsAgent 生成 search_results.json 与 news_articles.json
- NewsVerifier 明确读取 news_articles.json 并输出 verification.json
- SourceRanker 明确读取 verification.json 中的 sources 字段并输出 source_rank.json
- 禁止生成非冻结文件替代标准文件

交付要求：

- 所有文件路径与命名符合冻结协议
- 所有文件基于标准 JSON 结构读写
- 不允许用历史别名替代正式文件名

### Phase 3：流程编排适配

目标：让 ProductionController 与正式生产链路一致。

实施内容：

- 统一调度顺序：NewsAgent → NewsVerifier → SourceRanker
- 仅在控制器中管理执行状态与流程推进
- 检查关键文件生成情况
- 对关键步骤失败执行中断与错误保留

交付要求：

- 流程顺序固定
- 调度逻辑清晰
- 文件依赖显式化
- 不参与业务判断

### Phase 4：状态管理与问题追踪适配

目标：当前代码在后续 ProductionController 实现阶段，基于统一状态机进行状态管理。

实施内容：

- 统一执行状态：CREATED、RUNNING、SUCCESS、FAILED
- 关键失败必须保留 agent_name、error、timestamp
- 允许状态机用于恢复、排障和执行追踪
- 避免仅依赖隐式文件状态判断流程健康状况

交付要求：

- 状态機制可实现和追踪
- 关键失败可被定位
- 运行状态足以支持问题排查

### Phase 5：兼容性收口与回归验收

目标：使当前代码适配冻结架构而不超过冻结范围。

实施内容：

- 对照 01/02/03/04 冻结文档逐项核对
- 仅修正与冻结要求冲突的实现细节
- 验证无新增 Agent、无新增数据结构、无新增模块
- 确认当前实现仅覆盖正式 V2.0 最小链路

交付要求：

- 代码适配与冻结方案一致
- 任何回归均不破坏标准文件契约
- 不引入未来流程扩展

---

## 5. 实施优先级冻结

### P0 - 必须先做

- BaseAgent 基础接口统一
- NewsAgent 输出文件契约修正
- NewsVerifier 输入输出契约修正
- SourceRanker 来源评级输入输出修正
- ProductionController 流程顺序固定

### P1 - 必须同步完成

- 统一状态管理
- 错误上下文保留
- 关键文件依赖检查
- 执行中断规则

### P2 - 仅在当前代码范围内

- 避免采用非冻结接口绕过标准文件流
- 避免添加规划中 Agent
- 避免准备未来模块实现
- 避免对冻结字段结构进行扩展

---

## 6. 禁止事项

本实现路线图中，以下事项严格禁止：

- 新增未冻结 Agent
- 引入未来视频生产模块
- 扩展未冻结的数据结构
- 在正式链路中插入非正式步骤
- 在实现阶段绕过标准文件流
- 以隐式目录、默认目录或全局状态替代显式接口
- 将 SourceRanker 扩展为事实判断角色
- 将 NewsVerifier 退化成只读取 search_results.json 而不读取 news_articles.json
- 让 ProductionController 直接承担 NewsAgent、NewsVerifier、SourceRanker 的专业任务

---

## 7. 冻结结论

当前 V2.0 Implementation Roadmap Freeze 的正式结论如下：

- 实施工作仅限于现有代码适配，不扩展未来能力。
- 仅保留四个正式 Agent：BaseAgent、NewsAgent、NewsVerifier、SourceRanker。
- 不新增 Agent，不新增未来模块，不修改冻结的数据结构。
- 重点解决当前代码与已冻结架构之间的差距。
- ProductionController 仅作为编排层，负责调度、状态与文件依赖管理。
- 路线图以最小稳定 V2.0 生产链路为唯一目标，确保实现可控、可回归、可维护。

本文件作为 V2.0 Implementation Roadmap Freeze，保持当前已冻结基线的稳定性与规范边界。
