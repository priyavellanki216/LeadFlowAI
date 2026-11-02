
import pytest

from modules import lead_service
import database.db as db


@pytest.fixture
def isolated_database(tmp_path, monkeypatch):
    test_db_path = tmp_path / "lead_service_test.db"
    monkeypatch.setattr(db, "DB_PATH", test_db_path)
    db.initialize_db()
    return test_db_path


def test_lead_is_saved_when_ai_analysis_succeeds(
    isolated_database,
    monkeypatch,
):
    analysis = {
        "category": "Healthcare Technology",
        "summary": "Customer needs patient management software.",
        "intent": "Exploring healthcare automation.",
        "priority": "Hot",
        "reasoning": "Specific business requirement.",
        "missing_information": ["Budget"],
    }

    def mock_analyze_lead(**kwargs):
        return analysis

    monkeypatch.setattr(
        lead_service.ai_service,
        "analyze_lead",
        mock_analyze_lead,
    )

    result = lead_service.create_lead_with_analysis(
        "Sarah Johnson",
        "sarah@example.com",
        "Green Valley Healthcare",
        "Need an AI-powered patient management solution.",
    )

    assert result["analysis_saved"] is True
    assert result["error"] is None

    leads = db.get_recent_leads()

    assert len(leads) == 1
    assert leads[0]["id"] == result["lead_id"]
    assert leads[0]["priority"] == "Hot"
    assert leads[0]["ai_summary"] == analysis["summary"]


def test_lead_is_preserved_when_ai_analysis_fails(
    isolated_database,
    monkeypatch,
):
    def mock_analyze_lead(**kwargs):
        raise RuntimeError("Simulated Gemini service failure")

    monkeypatch.setattr(
        lead_service.ai_service,
        "analyze_lead",
        mock_analyze_lead,
    )

    result = lead_service.create_lead_with_analysis(
        "Failure Test Customer",
        "failure@example.com",
        "Test Company",
        "Testing AI failure handling.",
    )

    assert result["analysis_saved"] is False
    assert "Simulated Gemini service failure" in result["error"]

    leads = db.get_recent_leads()

    assert len(leads) == 1
    assert leads[0]["id"] == result["lead_id"]
    assert leads[0]["customer_name"] == "Failure Test Customer"
    assert leads[0]["email"] == "failure@example.com"
    assert leads[0]["ai_summary"] is None


def test_database_failure_is_not_hidden(
    isolated_database,
    monkeypatch,
):
    def mock_save_lead(**kwargs):
        raise RuntimeError("Simulated database failure")

    monkeypatch.setattr(db, "save_lead", mock_save_lead)

    with pytest.raises(RuntimeError, match="Simulated database failure"):
        lead_service.create_lead_with_analysis(
            "Database Failure Customer",
            "dbfailure@example.com",
            "Test Company",
            "Testing database failure.",
        )
