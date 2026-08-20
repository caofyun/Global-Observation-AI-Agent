# V2.0 Production Workflow Freeze

## 文档状态

V2.0 Production Workflow Freeze
Freeze Approved

---

## 1. Production Workflow Freeze目标

本文件基于已冻结的 Agent 基线 [docs/01_AGENT_BASELINE_FREEZE.md](docs/01_AGENT_BASELINE_FREEZE.md)、接口冻结方案 [docs/02_AGENT_INTERFACE_FREEZE.md](docs/02_AGENT_INTERFACE_FREEZE.md) 与数据结构冻结方案 [docs/03_DATA_STRUCTURE_FREEZE.md](docs/03_DATA_STRUCTURE_FREEZE.md)，在当前 V2.0 正式基线中冻结生产流程设计，目标是：

1. 明确当前唯一正式生产链路，避免流程漂移和隐式调用。
2. 统一 Agent 执行顺序、数据传递方式、输入输出文件边界。
3. 让 ProductionController 成为流程编排层，而非业务实现层。
4. 将标准化的 Agent 接口与标准化的数据文件串联成稳定的执行链。
5. 仅保留当前已实现、已冻结的最小生产流程，不扩展未来功能或未实现 Agent。

### 1.1 为什么需要生产流程冻结

在 V2.0 基线中，Agent 角色、接口字段、文件结构已完成冻结。若生产流程不冻结，则仍可能出现：

- Agent 执行顺序混乱
- 数据文件被错误写入或覆盖
- ProductionController 侵入专业 Agent 逻辑
- 生产链路依赖隐式目录或默认文件
- 未来功能被提前插入到当前正式流程中

因此，生产流程冻结的核心目的，是确保当前 V2.0 的执行链始终稳定、可验证、可维护。

### 1.2 冻结范围

本次冻结范围仅包含当前正式生产链路：

- BaseAgent
- NewsAgent
- NewsVerifier
- SourceRanker
- ProductionController

冻结对象：

- 执行顺序
- 文件流向
- Agent 边界
- 失败处理规则
- 局部控制职责

### 1.3 与前三个冻结文档的关系

- [docs/01_AGENT_BASELINE_FREEZE.md](docs/01_AGENT_BASELINE_FREEZE.md)：冻结正式 Agent 名称与职责边界。
- [docs/02_AGENT_INTERFACE_FREEZE.md](docs/02_AGENT_INTERFACE_FREEZE.md)：冻结 Agent 输入输出接口、文件名称、参数名称。
- [docs/03_DATA_STRUCTURE_FREEZE.md](docs/03_DATA_STRUCTURE_FREEZE.md)：冻结四类标准 JSON 数据结构。

本文件在上述三项基础上，进一步冻结当前 V2.0 的生产链路执行顺序与流程控制规则。

---

## 2. 当前V2.0生产流程总览

```text
用户输入主题
    ↓
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
```

### 2.1 正式生产链路

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

### 2.2 流程说明

- 用户首先提供主题输入。
- NewsAgent 负责搜索与正文整理，生成 search_results.json 与 news_articles.json。
- NewsVerifier 读取 news_articles.json，生成 verification.json。
- ProductionController 负责调度和状态管理，但不参与数据链路节点。
- SourceRanker 读取 verification.json 中的来源相关字段进行评级，并生成 source_rank.json。

---

## 3. ProductionController职责冻结

### 3.1 ProductionController 负责

ProductionController 负责：

- 创建项目流程
- 调度 Agent 执行顺序
- 管理 Agent 之间的数据传递
- 检查输入输出文件
- 记录执行状态

### 3.2 ProductionController 不负责

ProductionController 不负责：

- 新闻搜索
- 新闻核验
- 来源评级
- AI 判断逻辑

### 3.3 冻结边界

- ProductionController 只负责流程编排与状态管理。
- 不允许 ProductionController 直接嵌入 Agent 专业逻辑。
- 不允许 ProductionController 在未授权的情况下扩展非正式流程。

---

## 4. Agent执行顺序冻结

### Step 1: NewsAgent

输入：
- topic_keyword

输出：
- search_results.json
- news_articles.json

职责：
- 根据主题生成搜索关键词
- 执行搜索与发现整理
- 整理新闻正文数据
- 产出标准搜索和正文文件

### Step 2: NewsVerifier

输入：
- news_articles.json

输出：
- verification.json

职责：
- 读取正文数据
- 识别事实、冲突、不确定性
- 输出标准核验结果

### Step 3: SourceRanker

输入：
- verification.json读取：sources字段用途：来源质量评级

输出：
- source_rank.json

职责：
- 对来源进行质量评级
- 输出来源评级结果
- 不参与事实真实性判断

### 4.1 执行顺序冻结规则

- 当前 V2.0 正式顺序固定为：NewsAgent → NewsVerifier → SourceRanker。
- 所有 Step 均由 ProductionController 调度执行，Agent 之间不直接调用。
- 不允许插入未冻结 Agent。
- 不允许跳过标准文件生成步骤。
- 不允许在正式链路中重排步骤或破坏输出依赖。

---

## 5. 数据流转规则冻结

### 5.1 文件归属

search_results.json：
- 只允许 NewsAgent 生成

news_articles.json：
- 只允许 NewsAgent 生成

verification.json：
- 只允许 NewsVerifier 生成

source_rank.json：
- 只允许 SourceRanker 生成

### 5.2 数据流约束

- Agent 必须通过标准文件进行上下游传递。
- Agent 不允许读取未在接口协议中声明的非标准业务输入文件。
- Agent 不允许修改其他 Agent 输出文件。
- Agent 不允许绕过标准数据流直接传递隐式对象。
- 上下游必须显式通过文件或参数读取依赖项，而不能依赖隐式全局状态。

### 5.3 禁止事项

- Agent读取未在接口协议中声明的非标准业务输入文件
- Agent修改其他Agent输出文件
- Agent绕过标准数据流
- ProductionController 直接生成并替代 Agent 输出文件

---

## 6. Agent失败处理规则

### 6.1 基本原则

当 Agent 失败时，必须遵循 BaseAgent 接口语义返回执行状态与错误信息。

### 6.2 失败时的标准行为

- 需要返回 `status`
- 需要记录 `error`
- 允许记录失败原因，但不能伪造成功状态
- 若上游文件缺失或输入不可用，必须终止当前流程
- 若关键文件无法生成，应根据流程依赖决定是否终止

### 6.3 继续或终止

当前冻结规则：

- 关键步骤失败时，必须终止后续流程。
- 非关键状态可记录并持续，前提是不会破坏主流程逻辑。
- 任意 Agent 的失败，均应保留执行状态与错误上下文，保证可追溯。

### 6.4 与 BaseAgent 接口一致

失败处理必须保持与 BaseAgent 统一接口语义一致：

- `agent_name`
- `status`
- `result`
- `error`

> 当前文档冻结的是目标接口语义，实际代码必须在后续接口修复阶段满足该契约。

---

## 7. ProductionController与Agent边界

### 7.1 ProductionController

ProductionController 负责：

- 流程控制
- 执行次序编排
- 文件状态检查
- 执行日志与状态记录

### 7.2 Agent

Agent 负责：

- 专业任务执行
- 业务内容生成
- 文件输出
- 结果收敛

### 7.3 禁止事项

- ProductionController 包含业务判断逻辑。
- ProductionController 代替 NewsAgent 进行新闻搜索。
- ProductionController 代替 NewsVerifier 进行事实核验。
- ProductionController 代替 SourceRanker 进行来源评级。
- ProductionController 不作为生产节点参与数据流。

---

## 8. 当前V2.0生产流程限制

当前版本只支持以下正式链路：

新闻搜索
↓
新闻整理
↓
事实核验
↓
来源评级

### 8.1 当前版本允许的正式流程

- NewsAgent：搜索 + 正文整理
- NewsVerifier：事实核验
- SourceRanker：来源评级

### 8.2 当前版本不包含的未来扩展

以下 Agent 和流程均不属于当前正式 V2.0 生产链路：

- TopicScorer
- TopicSelector
- ScriptAgent
- StoryboardAgent
- MaterialAgent
- VideoAgent
- AudioSubtitleAgent
- ReviewAgent
- PublishAgent

这些属于 Future Extension，暂不纳入当前 V2.0 正式生产流程冻结。

---

## 9. Execution State Definition

### 9.1 统一执行状态冻结

ProductionController 统一管理执行状态，当前冻结状态集如下：

- CREATED
- RUNNING
- SUCCESS
- FAILED

### 9.2 失败状态要求

Agent 失败时必须包含：

- `agent_name`
- `error`
- `timestamp`

### 9.3 状态机约束

- `CREATED`：流程已生成，但尚未开始执行。
- `RUNNING`：流程或 Agent 正在执行。
- `SUCCESS`：关键任务已完成且对应输出已生成。
- `FAILED`：任务失败，必须保留错误信息与时间戳。
- 后续ProductionController实现阶段，应基于统一状态机进行执行状态管理和问题追踪，避免仅依赖隐式文件状态。

---

## 10. V2.0 Production Workflow Freeze总结

当前 V2.0 正式生产流程冻结结论如下：

- 当前唯一生产流程：NewsAgent → NewsVerifier → SourceRanker
- Agent 调用关系已冻结
- 数据流方向已冻结
- 生产控制职责已冻结
- 失败处理规则已冻结
- 生产链路仅保留当前已实现的最小稳定版本

最终冻结原则：

- 当前唯一生产链路稳定
- 文件流向稳定
- 执行顺序稳定
- Agent 边界稳定
- 数据流不允许绕过标准文件
- 不扩展未来功能
- 不修改代码、不改写测试、不引入未实现 Agent

本文件作为 V2.0 Production Workflow Freeze 文档，保持当前 V2.0 最小稳定基线原则。
