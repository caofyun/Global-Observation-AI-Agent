# StoryboardAgent Interface V2.0

状态：DESIGN FROZEN
日期：2026-08-26

## 1. 职责

StoryboardAgent 将已经人工确认的 ScriptAgent 脚本转换为结构化分镜，不重新选题、不重新写作、不重新事实核验。

## 2. 输入

机器权威输入：`script.json`。

必须包含：

- `schema_version`
- `status=SUCCESS`
- `selected_topic`
- `title`
- `script_segments`
- `fact_references`
- `human_confirmation`，且确认状态为允许制作

StoryboardAgent 不直接读取 TopicSelector 的原始输出作为选题依据。

## 3. 输出

机器权威产物：`storyboard.json`。

最小结构：

```json
{
  "schema_version": "2.0",
  "status": "SUCCESS",
  "topic": "...",
  "total_duration_seconds": 90,
  "scenes": [
    {
      "scene_id": "SCENE-001",
      "script_segment_id": "SEG-001",
      "duration_seconds": 8,
      "narration": "...",
      "visual": {
        "description": "...",
        "material_type": "news_footage"
      },
      "subtitle": "...",
      "sound_effect": null,
      "fact_references": []
    }
  ]
}
```

## 4. 追溯原则

每个 scene 必须能够追溯到一个或多个 `script_segment_id`。涉及事实陈述的场景应保留 `fact_references`，不得凭空新增事实。

## 5. 时间轴规则

- 每个 scene 必须有正数 `duration_seconds`。
- `total_duration_seconds` 必须等于所有 scene 时长之和。
- 不允许出现负数、零时长或无法解析的时间值。

## 6. 字段边界

- `narration`：来自脚本的旁白，不应自行扩写事实。
- `visual.description`：描述需要呈现的画面。
- `visual.material_type`：结构化标记素材需求类型。
- `subtitle`：对应旁白的字幕文本。
- `sound_effect`：可选音效需求。
- `fact_references`：继承脚本事实追溯。

## 7. 失败协议

以下情况必须返回统一 `FAILED`：

- `script.json` 缺失
- 输入不是 `SUCCESS`
- 人工确认缺失或未允许制作
- `script_segments` 缺失/为空
- 必需字段缺失
- 时间轴无法构建
- 上游 AI 生成失败

失败不得生成伪成功的 `storyboard.json`。

## 8. 人工审核边界

StoryboardAgent 输出后进入人工审核。人工审核负责确认：

1. 画面是否与旁白一致；
2. 素材类型是否可执行；
3. 时间轴是否合理；
4. 是否存在事实新增或事实漂移。

## 9. 非职责

StoryboardAgent 不负责：

- 新闻搜索
- 选题评分
- 选题决策
- 事实核验
- 脚本创作
- 实际素材下载
- 视频渲染
- 发布

## 10. 最小测试集合

至少覆盖：

1. 正常生成 storyboard；
2. 缺少 script.json；
3. 上游 FAILED；
4. 未人工确认；
5. script_segments 缺失；
6. scene 与 script segment 可追溯；
7. 总时长等于场景时长之和；
8. AI provider failure 返回 FAILED；
9. 不产生伪成功输出。
