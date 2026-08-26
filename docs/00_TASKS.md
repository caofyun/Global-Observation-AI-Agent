# Global-Observation-AI-Agent

# TASKS V2.3

更新时间：2026-08-26
项目状态：TASK-009 PASS / TASK-010 DESIGN FROZEN

---

# 1. 已完成任务

## TASK-006-X-04
状态：PASS

## TASK-007
状态：PASS

验收基线：Python 3.13 / pytest 9.1.1 / 72 passed / 0 failed / 0 pytest warnings / CI SUCCESS。

## TASK-008
状态：PASS / DESIGN FROZEN

内容：ScriptAgent V2.0 输入、输出、事实追溯、人工确认及失败协议冻结。

## TASK-009
状态：PASS / IMPLEMENTED + CI VERIFIED

实现：`src/agents/script_agent.py`
测试：`tests/test_script_agent.py`

最新 CI 验证：

- GitHub Actions Run `32926244406`
- Python 3.13.15
- pytest 9.1.1
- **83 passed in 8.44s**
- 0 failed
- 0 pytest warnings
- CI SUCCESS

注意：日志中的 Node.js 20 deprecation / punycode 信息属于 GitHub Actions 运行环境提示，不属于 pytest warning。

---

# 2. 当前任务

## TASK-010：StoryboardAgent 设计与接口冻结

状态：DESIGN FROZEN

目标：定义 ScriptAgent → StoryboardAgent 的稳定数据合同，禁止直接进入视频制作实现。

已完成：

- [x] 确认 ScriptAgent 为上游机器权威产物提供者
- [x] 确认 StoryboardAgent 不重新写作脚本
- [x] 定义 storyboard 的最小字段集合
- [x] 定义 scene 与 script segment 的追溯关系
- [x] 定义视觉素材需求的结构化边界
- [x] 定义旁白、画面、字幕、音效字段边界
- [x] 定义时间轴字段与总时长校验原则
- [x] 定义 SUCCESS / FAILED 边界
- [x] 定义人工审核节点

接口文档：`docs/agents/STORYBOARD_AGENT_INTERFACE_V2.0.md`

下一步：TASK-011 StoryboardAgent 实现与自动化测试。

---

# 3. 当前真实业务流水线

```text
NewsDiscovery
↓
NewsVerifier
↓
SourceRanker
↓
TopicScorer
↓
TopicSelector
↓
ScriptAgent（PASS）
↓
StoryboardAgent（设计冻结）
```

---

# 4. 当前数据边界

```text
TopicSelector
    ↓
topic_selection.json
    ↓
ScriptAgent
    ↓
script.json  ← 机器权威产物
script.md    ← 人工阅读产物
    ↓
人工确认
    ↓
StoryboardAgent
    ↓
storyboard.json
storyboard.xlsx / storyboard.md（视最终展示合同决定）
```

---

# 5. 下一任务

## TASK-011：StoryboardAgent 实现与自动化测试

前置条件：TASK-010 DESIGN FROZEN。

要求：

1. 严格按照接口冻结文档实现；
2. 不修改 ScriptAgent 及其他已冻结上游 Agent；
3. 新增 StoryboardAgent；
4. 新增自动化测试；
5. 保持统一 BaseAgent 返回协议；
6. 完成完整测试；
7. CI SUCCESS 后再冻结。

---

# 6. 长期路线

1. News Intelligence Chain
2. ScriptAgent
3. StoryboardAgent
4. MaterialAgent
5. Audio/Subtitle Agent
6. VideoAgent
7. ReviewAgent
8. PublishAgent

---

# 7. 执行规则

```text
需求
↓
设计冻结
↓
代码实现
↓
自动测试
↓
CI
↓
文档同步
↓
Git提交
↓
基线冻结
```
