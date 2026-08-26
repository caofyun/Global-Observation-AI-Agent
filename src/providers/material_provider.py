from abc import ABC, abstractmethod


class MaterialProvider(ABC):
    """Pluggable interface between MaterialAgent and material sources."""

    FOUND = "FOUND"
    NOT_FOUND = "NOT_FOUND"
    FAILED = "FAILED"

    @abstractmethod
    def search(self, asset_request):
        raise NotImplementedError

    @classmethod
    def normalize_result(cls, asset_request, result):
        if not isinstance(asset_request, dict):
            raise ValueError("asset_request 必须是对象")
        for field in ("asset_id", "scene_id", "script_segment_id"):
            if not asset_request.get(field):
                raise ValueError(f"asset_request 缺少{field}")
        if not isinstance(result, dict):
            raise ValueError("provider result 必须是对象")
        status = result.get("status")
        if status not in {cls.FOUND, cls.NOT_FOUND, cls.FAILED}:
            raise ValueError(f"非法Provider状态: {status}")
        return {
            "asset_id": asset_request["asset_id"],
            "status": status,
            "source": result.get("source"),
            "url": result.get("url"),
            "local_path": result.get("local_path"),
            "media_type": result.get("media_type"),
            "license": result.get("license"),
            "duration_seconds": result.get("duration_seconds"),
            "metadata": result.get("metadata", {}),
            "error": result.get("error"),
        }


class LocalMaterialProvider(MaterialProvider):
    """Deterministic provider used for local assets and automated tests."""

    def __init__(self, assets=None):
        self.assets = assets or {}

    def search(self, asset_request):
        asset_id = asset_request.get("asset_id") if isinstance(asset_request, dict) else None
        if not asset_id:
            raise ValueError("asset_request 缺少asset_id")
        asset = self.assets.get(asset_id)
        if asset is None:
            return self.normalize_result(asset_request, {"status": self.NOT_FOUND})
        result = dict(asset)
        result.setdefault("status", self.FOUND)
        result.setdefault("source", "local")
        return self.normalize_result(asset_request, result)
