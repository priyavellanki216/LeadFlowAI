import pytest

import database.db as db


@pytest.fixture
def test_database(tmp_path, monkeypatch):
    """
    Give every test its own temporary SQLite database.
    The real database and existing leads.db remain untouched.
    """
    test_db_path = tmp_path / "test_leads.db"

    monkeypatch.setattr(db, "DB_PATH", test_db_path)
    db.initialize_db()

    yield test_db_path


@pytest.fixture
def sample_lead(test_database):
    lead_id = db.save_lead(
        customer_name="Sarah Johnson",
        email="sarah@example.com",
        company="Green Valley Healthcare",
        enquiry="We need an AI-powered patient management solution."
    )

    return lead_id


def test_create_and_retrieve_lead(sample_lead):
    leads = db.get_recent_leads()

    assert len(leads) == 1

    lead = leads[0]

    assert lead["id"] == sample_lead
    assert lead["customer_name"] == "Sarah Johnson"
    assert lead["email"] == "sarah@example.com"
    assert lead["company"] == "Green Valley Healthcare"


def test_save_ai_analysis(sample_lead):
    analysis = {
        "category": "Healthcare Technology",
        "summary": "The customer needs an AI-powered patient management solution.",
        "intent": "Exploring healthcare automation.",
        "priority": "Hot",
        "reasoning": "The enquiry describes a specific business requirement.",
        "missing_information": ["Budget", "Expected implementation timeline"]
    }

    result = db.update_lead_analysis(sample_lead, analysis)

    assert result is True

    lead = db.get_recent_leads()[0]

    assert lead["category"] == "Healthcare Technology"
    assert lead["priority"] == "Hot"
    assert lead["ai_summary"] == analysis["summary"]
    assert lead["ai_intent"] == analysis["intent"]
    assert lead["ai_reasoning"] == analysis["reasoning"]


def test_missing_lead_id_does_not_update_analysis(test_database):
    analysis = {
        "category": "Software",
        "summary": "Test summary",
        "intent": "Test intent",
        "priority": "Warm",
        "reasoning": "Test reasoning",
        "missing_information": []
    }

    with pytest.raises(ValueError):
        db.update_lead_analysis(99999, analysis)


def test_save_followup_draft(sample_lead):
    draft = (
        "Subject: Follow-up on your enquiry\n\n"
        "Hi Sarah,\n\n"
        "Thank you for your interest. "
        "We would be happy to discuss your requirements.\n\n"
        "Best regards"
    )

    db.save_followup_draft(sample_lead, draft)

    lead = db.get_recent_leads()[0]
    history = db.get_followup_history(sample_lead)

    assert lead["followup_draft"] == draft
    assert len(history) == 1
    assert history[0]["draft"] == draft


def test_previous_followup_draft_is_preserved_in_history(sample_lead):
    first_draft = "Subject: First follow-up\n\nFirst draft."
    second_draft = "Subject: Updated follow-up\n\nSecond draft."

    db.save_followup_draft(sample_lead, first_draft)
    db.save_followup_draft(sample_lead, second_draft)

    lead = db.get_recent_leads()[0]
    history = db.get_followup_history(sample_lead)

    assert lead["followup_draft"] == second_draft
    assert len(history) == 2

    saved_drafts = {item["draft"] for item in history}

    assert first_draft in saved_drafts
    assert second_draft in saved_drafts


def test_missing_lead_id_does_not_save_followup(test_database):
    with pytest.raises(ValueError):
        db.save_followup_draft(
            99999,
            "Subject: Test\n\nTest follow-up."
        )


def test_empty_followup_draft_is_rejected(sample_lead):
    with pytest.raises(ValueError):
        db.save_followup_draft(sample_lead, "   ")


def test_failed_history_insert_rolls_back_draft_update(
    sample_lead,
    test_database
):
    original_draft = "Subject: Original\n\nOriginal draft."
    replacement_draft = "Subject: Replacement\n\nReplacement draft."

    db.save_followup_draft(sample_lead, original_draft)

    connection = db.get_connection()

    try:
        connection.execute("""
            CREATE TRIGGER reject_followup_history
            BEFORE INSERT ON follow_up_history
            BEGIN
                SELECT RAISE(ABORT, 'Simulated history insert failure');
            END;
        """)
        connection.commit()
    finally:
        connection.close()

    with pytest.raises(Exception):
        db.save_followup_draft(sample_lead, replacement_draft)

    lead = db.get_recent_leads()[0]
    history = db.get_followup_history(sample_lead)

    assert lead["followup_draft"] == original_draft
    assert len(history) == 1
    assert history[0]["draft"] == original_draft


def test_update_lead_information(sample_lead):
    updates = {
        "customer_name": "Sarah Williams",
        "email": "sarah.williams@example.com",
        "company": "Green Valley Medical",
        "enquiry": "We need an updated patient management solution.",
        "status": "Contacted",
    }

    result = db.update_lead(sample_lead, updates)

    assert result is True

    lead = db.get_recent_leads()[0]

    assert lead["customer_name"] == "Sarah Williams"
    assert lead["email"] == "sarah.williams@example.com"
    assert lead["company"] == "Green Valley Medical"
    assert lead["enquiry"] == updates["enquiry"]
    assert lead["status"] == "Contacted"


def test_update_lead_preserves_ai_analysis_and_followup(sample_lead):
    analysis = {
        "category": "Healthcare Technology",
        "summary": "Patient management requirement.",
        "intent": "Exploring automation.",
        "priority": "Hot",
        "reasoning": "Specific business requirement.",
        "missing_information": ["Budget"],
    }

    draft = "Subject: Follow-up\n\nThank you for your enquiry."

    db.update_lead_analysis(sample_lead, analysis)
    db.save_followup_draft(sample_lead, draft)

    db.update_lead(sample_lead, {"company": "Updated Healthcare"})

    lead = db.get_recent_leads()[0]
    history = db.get_followup_history(sample_lead)

    assert lead["company"] == "Updated Healthcare"
    assert lead["ai_summary"] == analysis["summary"]
    assert lead["priority"] == analysis["priority"]
    assert lead["followup_draft"] == draft
    assert len(history) == 1
    assert history[0]["draft"] == draft


def test_update_missing_lead_is_rejected(test_database):
    with pytest.raises(ValueError, match="not found"):
        db.update_lead(99999, {"company": "Unknown Company"})


def test_update_rejects_empty_required_fields(sample_lead):
    with pytest.raises(ValueError, match="customer_name cannot be empty"):
        db.update_lead(sample_lead, {"customer_name": "   "})


def test_update_rejects_unsupported_fields(sample_lead):
    with pytest.raises(ValueError, match="Unsupported lead fields"):
        db.update_lead(sample_lead, {"ai_summary": "Manually overwritten"})


def test_update_rejects_empty_update(sample_lead):
    with pytest.raises(ValueError, match="At least one field"):
        db.update_lead(sample_lead, {})
