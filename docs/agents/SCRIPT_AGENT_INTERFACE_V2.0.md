# ScriptAgent V2.0 接口规范

版本：V2.0  
状态：设计冻结  
任务：TASK-008

## 1. 定位

ScriptAgent 是内容生产层的视频脚本生成 Agent。它接收 TopicSelector 已明确选定的唯一主题，以及上游事实核验和来源评级产物，将“做什么”转换为“怎么讲”。

不负责：搜索、事实核验、来源评级、重新选题、分镜、素材、剪辑、发布。

## 2. 系统位置

```text
NewsDiscovery → NewsVerifier → SourceRanker → TopicScorer → TopicSelector → ScriptAgent → StoryboardAgent
```

核心边界：TopicSelector 决定做什么；ScriptAgent 决定怎么讲；StoryboardAgent 决定怎么画。

## 3. 输入合同

必需：

```text
05_选题决策/topic_selection.json
```

至少包含：`selected_topic`、`decision`、`selection_score`、`reason`。

事实与来源依据：

```text
02_事实核验/verification.json
03_来源评级/source_rank.json
```

实现时必须遵循当前项目实际目录合同，不得硬编码绝对路径。

`topic_selection.json` 决定主题；上游核验/来源数据决定可陈述事实。ScriptAgent 不得绕过上游合同自行联网搜索或凭模型常识补齐事实。

## 4. 输出合同

机器通信唯一权威产物：

```text
06_脚本/script.json
```

人工阅读表现层：

```text
06_脚本/script.md
```

两者必须表达同一份结果，不得形成第二套事实。

## 5. script.json 标准结构

```json
{
  "schema_version": "script.v2.0",
  "status": "SUCCESS",
  "project_id": "...",
  "selected_topic": "...",
  "decision": "进入制作",
  "title": "...",
  "duration_target_seconds": 90,
  "language": "zh-CN",
  "tone": "objective",
  "sections": [
    {"section_id": "hook", "type": "HOOK", "text": "..."},
    {"section_id": "body-01", "type": "BODY", "text": "..."},
    {"section_id": "ending", "type": "ENDING", "text": "..."}
  ],
  "fact_references": [
    {"claim_id": "claim-001", "source_id": "...", "verification_status": "VERIFIED"}
  ],
  "meta": {"generated_at": "...", "agent": "ScriptAgent", "version": "2.0"}
}
```

## 6. 内容规则

- 默认客观、克制、事实优先。
- 禁止无依据的夸张结论、情绪化判断、阴谋论和未经核验的因果关系。
- 标题必须围绕 `selected_topic`，不得引入上游不存在的新核心事实。
- 事实性陈述必须可追溯到上游核验/来源数据。
- 信息不足时减少表述或明确标注不确定性，不得伪装为事实。
- 默认目标时长 90 秒；覆盖时必须记录 `duration_target_seconds`。

## 7. 人工确认

```text
AI生成 → WAIT_USER_CONFIRM → 人工确认 → StoryboardAgent
```

未经确认不得标记为最终发布内容。

## 8. 状态与失败协议

遵循 BaseAgent 统一协议：`SUCCESS` / `FAILED`。

至少覆盖：缺少选题文件、缺少 selected_topic、decision 非“进入制作”、上游事实文件缺失、JSON 解析失败、输出写入失败、AI provider 失败。禁止吞错返回伪成功。

如果 `selected_topic` 缺失或 `decision != 进入制作`，必须失败；不得自行从排行榜选择其他主题。

## 9. 实现边界

代码：`src/agents/script_agent.py`  
测试：`tests/test_script_agent.py`

不得修改 BaseAgent、NewsAgent、NewsVerifier、SourceRanker、TopicScorer、TopicSelector 或已冻结数据合同；若发现阻塞性合同冲突，另立变更任务。

## 10. 最低测试要求

1. 正常输入 → SUCCESS
2. 缺少 topic_selection.json → FAILED
3. 缺少 selected_topic → FAILED
4. 非“进入制作” → FAILED
5. 上游事实文件缺失 → FAILED
6. AI provider 失败 → FAILED
7. 不把标题冒充正文
8. 输出包含 schema_version
9. 输出包含 fact_references
10. 输出可作为 StoryboardAgent 下一阶段输入

## 11. 冻结声明

本文件作为 TASK-008 ScriptAgent V2.0 的开发依据。任何超出职责边界的功能必须进入新的任务单。
