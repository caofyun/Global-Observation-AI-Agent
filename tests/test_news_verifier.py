import sys
import os


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.insert(0, PROJECT_ROOT)

from src.agents.news_verifier import NewsVerifier


def test_news_verifier_identifies_source_from_name_and_url():
    verifier = NewsVerifier()

    assert verifier.identify_source({"source": "Reuters"}) == "Reuters"
    assert (
        verifier.identify_source(
            {"url": "https://www.example.com/news/1"}
        )
        == "www.example.com"
    )
    assert verifier.identify_source({}) == "未知来源"


def test_news_verifier_normalizes_title():
    verifier = NewsVerifier()

    assert verifier.normalize_title(" 美国航母部署！ ") == "美国航母部署"
    assert verifier.normalize_title("US, Navy: Test") == "usnavytest"


def test_news_verifier_extracts_and_validates_ai_json():
    verifier = NewsVerifier()

    valid = {
        "confidence": "HIGH",
        "claims": [],
        "supporting_evidence": [],
        "conflicts": [],
        "uncertainties": [],
        "risk_notes": [],
        "ai_summary": "test",
        "human_review_required": True,
    }

    parsed = verifier.extract_json_from_text(
        "分析结果：\n```json\n" + str(valid).replace("'", '"') + "\n```"
    )

    assert parsed == valid
    assert verifier.validate_ai_result(parsed) is True


def test_news_verifier_rejects_invalid_ai_result():
    verifier = NewsVerifier()

    assert verifier.extract_json_from_text("not json") is None
    assert verifier.validate_ai_result({"confidence": "INVALID"}) is False
