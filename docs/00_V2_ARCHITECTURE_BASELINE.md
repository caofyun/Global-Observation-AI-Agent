# V2.0 Architecture Baseline

## 1. 基线目的

本文件用于记录项目在 V2.0 架构冻结阶段的当前基线。

V2.0 进入架构冻结阶段。在基线冻结完成前，不继续扩展新的 Agent，不增加新的核心数据字段，不进行大规模重构。本文件只记录现状、目标边界和未冻结项目，不构成代码修改方案。

## 2. 架构原则

- 文件驱动。
- Agent 职责独立。
- Agent 之间通过标准数据文件交互。
- `ProductionController` 负责流程编排。
- `ProjectManager` 负责项目生命周期和目录。
- Agent 负责自己的业务能力。
- 数据结构必须先定义，再开发代码。
- 测试必须可重复。
- 核心逻辑不允许依赖当前工作目录。
- 配置和 API Key 与代码分离。

以上内容是基线目标，不表示当前代码已经全部满足。

## 3. 当前 V2.0 Agent 清单

当前项目中已经存在的 Agent：

- `BaseAgent`
- `NewsAgent`
- `NewsVerifier`
- `SourceRanker`

规划中的 Agent（目前不视为已经实现）：

- `TopicScorer`
- `TopicSelector`
- `ScriptAgent`
- `StoryboardAgent`
- `MaterialAgent`
- `VideoAgent`
- `AudioSubtitleAgent`
- `ReviewAgent`
- `PublishAgent`

## 4. Agent 职责

以下内容是基线目标职责，不修改或重新解释现有代码行为。

- **NewsAgent**：负责新闻搜索、采集、基础整理。
- **NewsVerifier**：负责新闻结果基础验证、事实主张整理、冲突和不确定性分析，以及 AI 辅助验证。
- **SourceRanker**：负责新闻来源质量评级。不得将来源质量直接等同于新闻事实真实性。
- **ProductionController**：负责未来的生产流程编排，不承担具体新闻分析业务。
- **ProjectManager**：负责项目目录、项目元数据和项目生命周期管理。
- **BaseAgent**：提供统一 Agent 执行基础能力。

## 5. V2.0 标准数据文件

以下是候选核心数据对象。尚未冻结结构的对象明确标记为 `STATUS: NOT FROZEN`，本阶段不依据旧文档示例自行发明字段。

| 数据对象 | 状态 |
| --- | --- |
| `project.json` | STATUS: NOT FROZEN |
| `search_results.json` | STATUS: NOT FROZEN |
| `verification.json` | STATUS: NOT FROZEN |
| `ai_verification.json` | STATUS: NOT FROZEN |
| `source_rank.json` | STATUS: NOT FROZEN |
| `topic_score.json` | STATUS: NOT FROZEN |
| `script.md` | STATUS: NOT FROZEN |
| `storyboard` | STATUS: NOT FROZEN |
| `materials` | STATUS: NOT FROZEN |
| `editing_plan.md` | STATUS: NOT FROZEN |
| `voice.wav` | STATUS: NOT FROZEN |
| `subtitle.srt` | STATUS: NOT FROZEN |
| `review` | STATUS: NOT FROZEN |
| `publish` | STATUS: NOT FROZEN |

## 6. V2.0 标准工作流

当前目标工作流：

```text
ProjectManager
    ↓
NewsAgent
    ↓
search_results.json
    ↓
NewsVerifier
    ↓
verification.json + ai_verification.json
    ↓
SourceRanker
    ↓
source_rank.json
    ↓
TopicScorer
    ↓
 topic_score.json
    ↓
ScriptAgent
    ↓
StoryboardAgent
    ↓
MaterialAgent
    ↓
VideoAgent
    ↓
AudioSubtitleAgent
    ↓
ReviewAgent
    ↓
PublishAgent
```

当前完整工作流尚未实现。该流程是目标流程，不是当前代码已经完成的执行链路。

## 7. 状态体系

当前代码和文档存在多套状态名称，包括：

- `IDLE`
- `RUNNING`
- `COMPLETED`
- `ERROR`
- `WAIT_CONFIRM` 等工作流等待状态

本阶段只记录现有状态冲突，不修改代码，不选择其中任何一套作为最终标准。

最终状态体系：`STATUS: NOT FROZEN`

## 8. Agent 接口

V2.0 Agent 统一输入输出接口目前尚未冻结。当前特别存在以下接口命名冲突：

- `project_path`
- `verification_path`

不同 Agent 和测试脚本对项目目录路径、单个数据文件路径以及输入字典的使用方式并不统一。

最终接口：`STATUS: NOT FROZEN`

## 9. 项目目录

当前 `ProjectManager` 实际创建的目录结构为：

```text
projects/{project_name}/
├── project.json
├── 01_新闻资料/
├── 02_脚本/
├── 03_分镜/
├── 04_素材/
├── 05_制作/
├── 06_审核/
└── 07_发布/
```

README 等文档仍存在旧目录结构描述。最终目录规范：`STATUS: NOT FROZEN`。

## 10. 数据契约

V2.0 目前不能直接使用旧文档中的 JSON 示例作为最终标准。当前已知冲突包括：

- `source` / `name`
- `level` / `rank`
- `category` / `type`
- `search_results` / `results`
- `status` / `verification_status`
- `review.json` / `review_report.md`
- `materials.json` / `materials`

这些冲突只在本文件中记录，不在本阶段修复或自行选择最终字段。

最终数据契约：`STATUS: NOT FROZEN`

## 11. 测试基线

V2.0 最终要求：

- 使用 pytest。
- 可重复执行。
- 不依赖 `input()`。
- 不依赖当前工作目录。
- 网络测试与单元测试分离。
- AI API 测试与普通测试分离。
- 使用 fixture 和 mock。
- 测试不能污染真实 `projects/` 目录。

当前 `tests/` 目录尚未满足以上要求。

状态：`STATUS: NOT FROZEN`

## 12. 路径基线

V2.0 要求所有核心路径能够从不同工作目录稳定运行。核心逻辑禁止依赖 `os.getcwd()`、未定义的相对路径或启动位置隐含的项目目录假设。

当前 `SourceRanker` 等模块存在路径风险，尤其是来源数据库加载和输出路径推导。

状态：`STATUS: NOT FROZEN`

## 13. 配置和安全基线

- API Key 不得进入代码。
- `.env` 不得提交 Git。
- 配置与代码分离。
- 真实 API 测试与自动化测试分离。
- 本阶段只记录规范，不修改配置。

## 14. 架构冻结规则

在基线正式冻结之前，禁止：

- 新增 Agent 功能。
- 扩展 SourceRanker 评分模型。
- 开发 `TopicScorer`。
- 开发 `ScriptAgent`。
- 开发 `VideoAgent`。
- 开发自动发布。
- 增加核心 JSON 字段。
- 进行大规模代码重构。

## 15. 当前已知问题

本节只记录问题类别，不修复问题：

- Agent 接口不统一。
- 数据结构不统一。
- 状态不统一。
- 目录不统一。
- 测试不统一。
- `SourceRanker` 的 `aliases` 未使用。
- `category` / `type` 冲突。
- 路径依赖。
- `ProductionController` 尚未真正调度 Agent。
- 文档与代码状态不一致。

## 16. 基线状态

V2.0 Architecture Baseline：`STATUS: DRAFT`

原因：架构规范已经建立，但 Agent 接口、数据结构、状态、目录和测试基线仍需要逐项冻结。

本文件只作为 V2.0 架构基线草案：

- 不得根据本文件自动修改代码。
- 不得根据本文件自动修复上述问题。
- 不得将规划中的 Agent 视为已经实现。
- 不得将本文件中的候选数据对象视为已经冻结的最终契约。
