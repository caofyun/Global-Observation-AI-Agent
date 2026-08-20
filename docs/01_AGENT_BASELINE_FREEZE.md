# V2.0 Agent Architecture Baseline

## Freeze Candidate Approved

### 文档状态

V2.0 Agent Architecture Baseline
Freeze Candidate Approved

---

## 1. Agent 标准名称冻结表

| 标准名称 | 当前代码类名 | 当前文件路径 | 当前职责 | 当前状态 | 冻结状态 |
| --- | --- | --- | --- | --- | --- |
| BaseAgent | BaseAgent | src/agents/base_agent.py | 提供统一 Agent 基础接口、执行入口、状态管理与抽象协议 | 已实现 | 冻结 |
| NewsAgent | NewsAgent | src/agents/news_agent.py | 新闻选题处理、关键词生成、搜索与结果汇总 | 已实现 | 冻结 |
| NewsVerifier | NewsVerifier | src/agents/news_verifier.py | 新闻事实核验、来源分析、冲突识别、AI 辅助判断 | 已实现 | 冻结 |
| SourceRanker | SourceRanker | src/agents/source_ranker.py | 新闻来源评级、质量分析与风险提示 | 已实现 | 冻结 |

---

## 2. Agent 职责冻结表

| 标准名称 | 冻结职责说明 |
| --- | --- |
| BaseAgent | 提供所有 Agent 的统一基础能力，包括执行契约、状态管理与错误处理。 |
| NewsAgent | 负责新闻主题输入、搜索关键词构造、搜索执行与结果处理。 |
| NewsVerifier | 负责核验搜索结果的有效性、事实主张整理、冲突分析、不确定性判断与 AI 辅助验证。 |
| SourceRanker | 负责对来源进行评级、评估可信度和质量风险，输出来源质量分析结果。 |

---

## 3. Agent 实现状态表

| 标准名称 | 实现状态 | 说明 |
| --- | --- | --- |
| BaseAgent | 已实现 | 在代码中存在实际类定义，并作为所有 Agent 的基础类。 |
| NewsAgent | 已实现 | 在代码中存在实际类定义，具备搜索与资料整理能力。 |
| NewsVerifier | 已实现 | 在代码中存在实际类定义，具备事实核验辅助分析逻辑。 |
| SourceRanker | 已实现 | 在代码中存在实际类定义，可进行来源评级。 |
| NewsSourceRanker | 未实现 | 仅为命名候选，不存在独立代码实现。 |
| TopicScorer | 未实现 | 规划中 Agent，未落地。 |
| TopicSelector | 未实现 | 规划中 Agent，未落地。 |
| ScriptAgent | 未实现 | 规划中 Agent，未落地。 |
| StoryboardAgent | 未实现 | 规划中 Agent，未落地。 |
| MaterialAgent | 未实现 | 规划中 Agent，未落地。 |
| VideoAgent | 未实现 | 规划中 Agent，未落地。 |
| AudioSubtitleAgent | 未实现 | 规划中 Agent，未落地。 |
| ReviewAgent | 未实现 | 规划中 Agent，未落地。 |
| PublishAgent | 未实现 | 规划中 Agent，未落地。 |

---

## 4. Agent 冻结状态表

| 标准名称 | 实现状态 | 冻结状态 | 说明 |
| --- | --- | --- | --- |
| BaseAgent | 已实现 | 冻结 | 属于当前 V2.0 正式基线候选 Agent，后续禁止随意改名或重构核心接口。 |
| NewsAgent | 已实现 | 冻结 | 属于当前 V2.0 正式基线候选 Agent，职责边界应保持稳定。 |
| NewsVerifier | 已实现 | 冻结 | 属于当前 V2.0 正式基线候选 Agent，验证输出结构需保持稳定。 |
| SourceRanker | 已实现 | 冻结 | 作为正式名称保留，后续不得扩展为不一致的重命名方案。 |
| NewsSourceRanker | 未实现 | 未冻结 | 仅为命名候选，不属于正式基线。 |
| TopicScorer | 未实现 | 未冻结 | 规划中 Agent，延后纳入正式基线。 |
| TopicSelector | 未实现 | 未冻结 | 规划中 Agent，延后纳入正式基线。 |
| ScriptAgent | 未实现 | 未冻结 | 规划中 Agent，延后纳入正式基线。 |
| StoryboardAgent | 未实现 | 未冻结 | 规划中 Agent，延后纳入正式基线。 |
| MaterialAgent | 未实现 | 未冻结 | 规划中 Agent，延后纳入正式基线。 |
| VideoAgent | 未实现 | 未冻结 | 规划中 Agent，延后纳入正式基线。 |
| AudioSubtitleAgent | 未实现 | 未冻结 | 规划中 Agent，延后纳入正式基线。 |
| ReviewAgent | 未实现 | 未冻结 | 规划中 Agent，延后纳入正式基线。 |
| PublishAgent | 未实现 | 未冻结 | 规划中 Agent，延后纳入正式基线。 |

---

## 5. 延后 Agent 列表

以下 Agent 不纳入当前 V2.0 正式基线，暂定延后：

- TopicScorer
- TopicSelector
- ScriptAgent
- StoryboardAgent
- MaterialAgent
- VideoAgent
- AudioSubtitleAgent
- ReviewAgent
- PublishAgent
- NewsSourceRanker

说明：
- 这些名称主要存在于规划、扩展或文档中的未来设计阶段。
- 它们尚未形成稳定的代码实现与统一注册规则。
- 因此，不视为正式冻结基线成员。

---

## 6. 命名冲突处理规则

### 6.1 命名冲突原则

1. 代码中真实存在的类名优先于文档中的候选名称。
2. 规划中的名称不能直接覆盖已实现的正式类名。
3. 任何新命名必须在冻结前完成统一确认，避免分裂的 Agent 角色命名。
4. 设计文档中的名称与代码类名必须保持一一对应，除非明确标识为“Future Extension”。

### 6.2 具体冲突处理

- SourceRanker 与 NewsSourceRanker 的冲突处理规则：
  - 代码中已确认真实命名为 SourceRanker。
  - NewsSourceRanker 仅作为候选或历史命名，不作为正式名称。
  - 若未来确实需要保留 NewsSourceRanker，则必须在下一轮架构核准中显式声明，并同步更新设计文档与代码命名。

### 6.3 冻结名约束

- 正式基线中的 Agent 名称必须保持稳定。
- 不得在正式冻结后，以“重命名/别名/占位命名”的方式随意替换当前代码类名。
- 规划项必须被单独标记为 Future Extension，而不能被混入正式基线。

---

## 7. SourceRanker 作为正式名称说明

SourceRanker 是当前代码中的正式名称，且应作为 V2.0 正式基线中的标准命名。

明确要求：
- 代码实现中使用 SourceRanker。
- 设计文档中使用 SourceRanker。
- 正式冻结的基线名称应保持为 SourceRanker。
- NewsSourceRanker 不得作为正式代码命名进入当前 V2.0 基线。

原因：
- SourceRanker 已在实际代码里实现并使用。
- 该名称具有唯一性、稳定性和可追溯性。
- 使用 SourceRanker 可避免命名冲突、混淆和后续扩展时的二义性。

---

## 8. 冻结结论

V2.0正式基线 Agent：

- BaseAgent
- NewsAgent
- NewsVerifier
- SourceRanker

其他规划Agent：

- Future Extension

结论：
- 当前正式基线仅保留已实现且职责清晰的四个 Agent。
- 所有规划中 Agent 暂不纳入正式冻结范围。
- SourceRanker 作为正式名称固定下来，NewsSourceRanker 仅作为候选命名，不纳入正式基线。
- 在冻结后，只有四个 Agent 可作为当前 V2.0 稳定边界的正式成员。
