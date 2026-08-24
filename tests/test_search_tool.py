import sys
import os


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.insert(0, PROJECT_ROOT)

from src.utils.search_tool import SearchTool


def test_search_tool_initialization():
    search_tool = SearchTool()
    assert search_tool.name == "新闻搜索工具"


def test_search_tool_rejects_empty_keyword():
    search_tool = SearchTool()

    try:
        search_tool.search("   ")
    except ValueError as exc:
        assert "搜索关键词不能为空" in str(exc)
    else:
        raise AssertionError("empty keyword should fail")
