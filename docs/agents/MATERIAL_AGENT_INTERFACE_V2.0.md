# MaterialAgent Interface V2.0

状态：DESIGN FROZEN
日期：2026-08-26

## 1. 职责

MaterialAgent 将已经人工确认的 `storyboard.json` 转换为结构化素材需求与素材检索任务，不负责实际视频剪辑、渲染或发布。

MaterialAgent 的核心目标是回答：每个 scene 需要什么素材、素材应满足什么约束、素材从哪里获得以及当前素材状态是什么。

## 2. 输入

机器权威输入：`storyboard.json`。

必须包含：

- `schema_version`
- `status=SUCCESS`
- `topic`
- `scenes`
- 每个 scene 的 `scene_id`
- `script_segment_id`
- `duration_seconds`
- `visual.description`
- `visual.material_type`
- `fact_references`（如有）

MaterialAgent 不重新读取新闻搜索结果，不重新进行选题，不修改脚本或分镜。

## 3. 输出

机器权威产物：`material_plan.json`。

最小结构：

```json
{
  "schema_version": "2.0",
  "status": "SUCCESS",
  "topic": "...",
  "source_storyboard": "storyboard.json",
  "statistics": {
    "scene_count": 1,
    "asset_request_count": 1,
    "ready_count": 0,
    "unresolved_count": 1
  },
  "asset_requests": [
    {
      "asset_id": "ASSET-001",
      "scene_id": "SCENE-001",
      "script_segment_id": "SEG-001",
      "asset_type": "news_footage",
      "description": "...",
      "search_query": "...",
      "duration_seconds": 8,
      "fact_references": [],
      "source": null,
      "url": null,
      "license": null,
      "status": "REQUESTED"
    }
  ]
}
```

## 4. 素材类型

V2.0 最小标准类型：`news_footage`、`photo`、`map`、`chart`、`document`、`generic_broll`、`text_graphic`。

不得使用未定义的素材类型；扩展类型必须先更新数据合同。

## 5. 追溯原则

每个素材请求必须追溯到 `asset_id → scene_id → script_segment_id → fact_references`。MaterialAgent 不得因为生成素材搜索词而新增新闻事实。

## 6. 来源与版权原则

素材来源结构化记录：`source`、`url`、`license`。尚未实际获取素材时允许为 `null`。不得虚构素材来源、URL 或版权许可。

## 7. 状态协议

单个素材请求：`REQUESTED`、`READY`、`UNRESOLVED`、`FAILED`。

整体 Agent：`SUCCESS` / `FAILED`。

`UNRESOLVED` 表示某个素材尚未找到可用资源，不等同于 Agent 执行失败。输入合同无效、文件缺失或 AI provider 失败时必须返回 `FAILED`，不得生成伪成功产物。

## 8. 人工审核边界

MaterialAgent 输出后进入人工审核，确认素材匹配度、来源可信度、URL、授权/许可、版权风险以及替换/补充需求。

## 9. 非职责

MaterialAgent 不负责新闻搜索与事实核验、选题决策、脚本创作、修改分镜、视频剪辑、视频渲染、音频制作或发布。

## 10. 最小测试集合

至少覆盖：正常生成；缺少 `storyboard.json`；上游 `FAILED`；storyboard 缺少 scenes；scene 缺少素材类型；scene 与 asset request 可追溯；不虚构 source/url/license；AI provider failure 返回 `FAILED`；不产生伪成功输出；`UNRESOLVED` 不误报 Agent failure。
