# Material Provider Interface V2.0

状态：DESIGN FROZEN
日期：2026-08-26

## 1. 目标

Material Provider 是 `MaterialAgent` 与实际素材获取能力之间的适配层。

```text
MaterialAgent
    ↓ material_plan.json
MaterialProvider
    ↓ provider request
实际素材源 / 本地素材库 / API
    ↓
MaterialProviderResult
    ↓
素材验证 / 人工版权确认
```

MaterialAgent 不直接绑定具体网站、API、下载器或存储实现。

## 2. 输入合同

Provider 接收单个 `asset_request`，至少包含：

- `asset_id`
- `scene_id`
- `script_segment_id`
- `asset_type`
- `description`
- `search_query`
- `duration_seconds`
- `fact_references`

Provider 不得改变 `scene_id`、`script_segment_id` 或 `fact_references` 的语义。

## 3. 输出合同

Provider 必须返回结构化结果：

```json
{
  "asset_id": "ASSET-001",
  "status": "FOUND",
  "source": "provider-name",
  "url": "https://example.invalid/asset",
  "local_path": null,
  "media_type": "video",
  "license": null,
  "duration_seconds": 8,
  "metadata": {},
  "error": null
}
```

最小状态：`FOUND`、`NOT_FOUND`、`FAILED`。

Provider 不得把 `NOT_FOUND` 伪装成 `FOUND`。

## 4. 来源与版权

Provider 可以提供来源元数据，但不得凭空生成版权许可。

`url`、`license`、`local_path` 允许为 `null`。无法确认许可状态时必须保持 `license=null`，交由后续人工审核。

## 5. 下载边界

V2.0 Provider 可以搜索或获取候选素材，但默认不承担最终发布授权判断。是否允许下载、保存、剪辑和发布，由后续素材审核策略决定。

Provider 不得绕过网站访问控制、付费限制、robots/服务条款或版权限制。

## 6. 不允许的职责

MaterialProvider 不负责新闻事实核验、选题、脚本生成、分镜修改、自动判断版权合法性、视频剪辑、视频渲染或发布。

## 7. 可插拔设计

允许实现多个 Provider：

```text
MaterialProvider
├── LocalMaterialProvider
├── NewsMediaProvider
├── ImageProvider
├── MapProvider
└── ChartProvider
```

上层只依赖统一接口，不依赖具体 Provider。

## 8. 失败协议

Provider 异常必须显式返回 `FAILED` 或由上层统一转换为 `FAILED`。不得返回空对象并被上层误判为成功。

## 9. 最小测试集合

至少覆盖：正常 FOUND；NOT_FOUND；Provider exception → FAILED；不虚构 URL；不虚构 license；保留 asset_id / scene_id / script_segment_id；多 Provider 可替换；不修改 MaterialAgent 的原始素材需求。

## 10. V2.0 冻结原则

第一阶段只冻结 Provider 接口，不绑定具体第三方平台。具体 Provider 在后续任务中单独实现和测试。
