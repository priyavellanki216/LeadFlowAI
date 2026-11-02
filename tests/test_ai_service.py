
import json

import pytest

from modules.ai_service import _parse_analysis_response


VALID_ANALYSIS = {
    "category": "Healthcare Technology",
    "summary": "The customer needs a patient management solution.",
    "intent": "Exploring healthcare automation.",
    "priority": "Hot",
    "reasoning": "The enquiry describes a specific business requirement.",
    "missing_information": ["Budget", "Implementation timeline"],
}


def test_parse_valid_analysis():
    result = _parse_analysis_response(json.dumps(VALID_ANALYSIS))

    assert result["category"] == "Healthcare Technology"
    assert result["priority"] == "Hot"
    assert result["intent"] == VALID_ANALYSIS["intent"]
    assert result["missing_information"] == ["Budget", "Implementation timeline"]


def test_parse_analysis_with_markdown_code_fence():
    response = "```json\n" + json.dumps(VALID_ANALYSIS) + "\n```"

    result = _parse_analysis_response(response)

    assert result["priority"] == "Hot"


def test_reject_invalid_json():
    with pytest.raises((ValueError, json.JSONDecodeError)):
        _parse_analysis_response("{invalid json")


def test_reject_invalid_priority():
    invalid = VALID_ANALYSIS.copy()
    invalid["priority"] = "Urgent"

    with pytest.raises(ValueError):
        _parse_analysis_response(json.dumps(invalid))


def test_reject_invalid_category():
    invalid = VALID_ANALYSIS.copy()
    invalid["category"] = "Unknown Category"

    with pytest.raises(ValueError):
        _parse_analysis_response(json.dumps(invalid))


def test_reject_missing_required_field():
    invalid = VALID_ANALYSIS.copy()
    del invalid["summary"]

    with pytest.raises(ValueError):
        _parse_analysis_response(json.dumps(invalid))


def test_reject_empty_summary():
    invalid = VALID_ANALYSIS.copy()
    invalid["summary"] = "   "

    with pytest.raises(ValueError):
        _parse_analysis_response(json.dumps(invalid))


def test_reject_invalid_missing_information():
    invalid = VALID_ANALYSIS.copy()
    invalid["missing_information"] = "Budget"

    with pytest.raises(ValueError):
        _parse_analysis_response(json.dumps(invalid))
