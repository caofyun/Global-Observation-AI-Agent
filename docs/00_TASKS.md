# Global-Observation-AI-Agent

# TASKS V2.2

更新时间：2026-08-26
项目状态：TASK-008 设计冻结

---

# 1. 已完成任务

## TASK-006-X-04
状态：PASS

## TASK-007
状态：PASS

验收基线：Python 3.13 / pytest 9.1.1 / 72 passed / 0 failed / 0 pytest warnings / CI SUCCESS。

---

# 2. 当前任务

## TASK-008：ScriptAgent 设计与接口冻结

状态：DESIGN FROZEN

已完成：

- [x] 审查 TopicSelector → ScriptAgent 边界
- [x] 定义 ScriptAgent 单一职责
- [x] 定义输入合同
- [x] 定义输出合同
- [x] 定义 script.json 机器通信标准
- [x] 定义 script.md 人工阅读边界
- [x] 定义事实追溯规则
- [x] 定义人工确认节点
- [x] 定义 SUCCESS / FAILED 错误边界
- [x] 定义测试最低集合
- [x] 创建 `docs/agents/SCRIPT_AGENT_INTERFACE_V2.0.md`

下一步：TASK-009 ScriptAgent 实现与自动化测试。

TASK-009 开始前不得修改 TopicSelector 或已冻结上游 Agent。

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
ScriptAgent（设计冻结）
↓
StoryboardAgent（未开发）
```

---

# 4. ScriptAgent 数据边界

```text
05_选题决策/topic_selection.json
        +
02_事实核验/verification.json
03_来源评级/source_rank.json
        ↓
ScriptAgent
        ↓
06_脚本/script.json   ← 机器权威产物
06_脚本/script.md     ← 人工阅读产物
        ↓
人工确认
        ↓
StoryboardAgent
```

---

# 5. 下一任务

## TASK-009：ScriptAgent 实现与自动化测试

前置条件：TASK-008 DESIGN FROZEN。

要求：

1. 严格按照接口冻结文档实现；
2. 不修改已冻结上游 Agent；
3. 新增 `src/agents/script_agent.py`；
4. 新增 `tests/test_script_agent.py`；
5. 保持统一 BaseAgent 返回协议；
6. 完成完整测试；
7. CI SUCCESS 后再冻结。

---

# 6. 长期路线

1. ScriptAgent
2. StoryboardAgent
3. MaterialAgent
4. Audio/Subtitle Agent
5. VideoAgent
6. ReviewAgent
7. PublishAgent

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
