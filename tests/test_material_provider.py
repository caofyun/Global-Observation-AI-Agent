import pytest

from src.providers.material_provider import LocalMaterialProvider, MaterialProvider


@pytest.fixture
def request_data():
    return {
        "asset_id": "ASSET-001",
        "scene_id": "SCENE-001",
        "script_segment_id": "SEG-001",
        "asset_type": "photo",
        "description": "测试图片",
        "search_query": "测试图片",
        "duration_seconds": 3,
        "fact_references": ["FACT-001"],
    }


def test_found_preserves_traceability(request_data):
    provider = LocalMaterialProvider({"ASSET-001": {"status": "FOUND", "source": "local", "local_path": "assets/test.jpg", "media_type": "image"}})
    result = provider.search(request_data)
    assert result["status"] == MaterialProvider.FOUND
    assert result["asset_id"] == "ASSET-001"
    assert result["source"] == "local"
    assert result["local_path"] == "assets/test.jpg"


def test_not_found_is_explicit(request_data):
    result = LocalMaterialProvider().search(request_data)
    assert result["status"] == MaterialProvider.NOT_FOUND
    assert result["url"] is None
    assert result["license"] is None


def test_provider_never_invents_license(request_data):
    result = LocalMaterialProvider({"ASSET-001": {"status": "FOUND"}}).search(request_data)
    assert result["license"] is None
    assert result["url"] is None


def test_normalize_rejects_missing_traceability(request_data):
    broken = dict(request_data)
    del broken["scene_id"]
    with pytest.raises(ValueError):
        MaterialProvider.normalize_result(broken, {"status": "FOUND"})


def test_normalize_rejects_invalid_status(request_data):
    with pytest.raises(ValueError):
        MaterialProvider.normalize_result(request_data, {"status": "SUCCESS"})


def test_normalize_rejects_non_object_result(request_data):
    with pytest.raises(ValueError):
        MaterialProvider.normalize_result(request_data, None)


def test_provider_result_cannot_change_asset_id(request_data):
    result = MaterialProvider.normalize_result(request_data, {"status": "FOUND", "asset_id": "FAKE-ID", "source": "local"})
    assert result["asset_id"] == request_data["asset_id"]


def test_provider_exception_is_visible():
    class BrokenProvider(MaterialProvider):
        def search(self, asset_request):
            raise RuntimeError("provider unavailable")

    with pytest.raises(RuntimeError, match="provider unavailable"):
        BrokenProvider().search({"asset_id": "ASSET-001", "scene_id": "SCENE-001", "script_segment_id": "SEG-001"})


def test_multiple_local_providers_are_replaceable(request_data):
    first = LocalMaterialProvider({"ASSET-001": {"status": "FOUND", "source": "first"}})
    second = LocalMaterialProvider({"ASSET-001": {"status": "FOUND", "source": "second"}})
    assert first.search(request_data)["source"] != second.search(request_data)["source"]
