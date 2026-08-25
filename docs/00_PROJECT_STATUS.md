# 环球观察速递 AI Agent 工厂

# PROJECT_STATUS.md V2.1

版本：V2.1
更新时间：2026-08-25
项目状态：工程化基线同步完成

---

# 一、当前基线

GitHub 主分支：`main`

基线提交：`4c0dcb76de218c649418a7d4941583a1b0d461d9`

TASK-006-X-04：PASS

本地测试基线：

```text
72 passed
0 failed
3 warnings
44.53s
```

CI：Pipeline Contract Check SUCCESS。

说明：72 passed 为当前已确认的测试基线；3 warnings 尚未在本次状态同步中宣称已清零，后续单独处理。

---

# 二、当前已实现工程组件

## Core

- BaseAgent
- ProjectManager
- ProductionController
- Pipeline Runner / Discovery Pipeline Adapter

## News Intelligence

- NewsAgent
- NewsVerifier
- SourceRanker
- TopicScorer
- TopicSelector
- AIModelClient
- SearchTool

当前实际新闻智能链：

```text
NewsDiscovery
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
    ↓
TopicScorer
    ↓
topic_score.json
    ↓
TopicSelector
    ↓
topic_selection.json
```

TopicScorer V2.0 与 TopicSelector V2.0 已存在代码、接口文档及测试覆盖；因此不再将二者标记为“未开始”。

---

# 三、当前生产链边界

当前已经形成的是：

**新闻发现 → 事实核验 → 来源评级 → 热点评分 → 选题决策**

当前仍未实现的内容生产 Agent：

- ScriptAgent
- StoryboardAgent
- MaterialAgent
- AudioSubtitleAgent / VoiceAgent
- VideoAgent
- ReviewAgent
- PublishAgent

因此，项目当前仍属于“新闻智能链完成、内容生产链待开发”的工程阶段。

---

# 四、Agent 注册表（当前真实状态）

| 组件 | 当前状态 | 说明 |
|---|---|---|
| BaseAgent | FROZEN | 统一 Agent 基础接口 |
| SearchTool | STABLE | 新闻搜索工具 |
| NewsAgent | STABLE | 新闻发现/结构化 |
| NewsVerifier | STABLE | 新闻事实核验 |
| SourceRanker | STABLE | 新闻来源评级 |
| TopicScorer | STABLE | 热点评分 |
| TopicSelector | STABLE | 选题决策 |
| AIModelClient | STABLE | 统一 AI 调用 |
| ProjectManager | STABLE | 项目管理 |
| ProductionController | STABLE | 流程控制基础能力 |

---

# 五、数据合同基线

当前关键产物：

```text
news_articles.json
verification.json
ai_verification.json
source_rank.json
topic_score.json
topic_selection.json
```

数据通过明确文件接口衔接，禁止隐式跨 Agent 传递。

---

# 六、工程质量基线

当前重点：

1. Agent 统一 SUCCESS / FAILED 返回协议
2. Pipeline Contract Check
3. Agent 间数据合同一致性
4. 自动化测试
5. 文档与代码状态同步

TASK-006-X-04 已完成统一失败返回协议，当前主分支以该提交作为新的工程基线。

---

# 七、当前任务阶段

TASK-007：V2.0 项目状态同步与开发基线冻结

状态：执行中

目标：

- 校准代码真实状态
- 校准 Agent 注册表
- 校准实际数据流水线
- 更新 PROJECT_STATUS
- 更新 TASKS
- 更新 CHANGELOG
- 固化 72 passed 测试基线
- 单独识别并处理 3 个 pytest warnings

---

# 八、下一开发原则

在 TASK-007 完成并冻结后，不直接盲目开发新 Agent。

下一功能任务必须按照：

```text
需求
↓
接口/数据合同
↓
设计文档
↓
代码
↓
自动测试
↓
CI
↓
文档同步
↓
Git 提交
↓
基线冻结
```

下一候选业务 Agent：ScriptAgent。

但 ScriptAgent 必须在新的任务单批准后进入开发。
