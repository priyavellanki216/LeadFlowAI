
import logging

from database import db
from modules import ai_service

logger = logging.getLogger(__name__)


class AnalysisPersistenceError(Exception):
    """Raised when AI analysis is generated but cannot be saved."""

    def __init__(self, lead_id):
        self.lead_id = lead_id
        super().__init__(
            f"AI analysis could not be saved for lead ID {lead_id}."
        )


def create_lead_with_analysis(
    customer_name,
    email,
    company,
    enquiry,
):
    """
    Save the lead first, then generate and persist AI analysis.

    AI generation failures do not delete the lead.
    Database persistence failures are reported separately.
    """

    # STEP 1: Persist the original enquiry.
    lead_id = db.save_lead(
        customer_name=customer_name,
        email=email,
        company=company,
        enquiry=enquiry,
    )

    # STEP 2: Generate AI analysis.
    try:
        analysis = ai_service.analyze_lead(
            customer_name=customer_name,
            company=company,
            enquiry=enquiry,
        )

    except Exception as exc:
        logger.exception(
            "AI analysis generation failed for lead ID %s.",
            lead_id,
        )

        return {
            "lead_id": lead_id,
            "analysis_saved": False,
            "analysis": None,
            "error": str(exc),
        }

    # STEP 3: Persist AI analysis separately.
    # A database error here must not be classified as an AI failure.
    try:
        db.update_lead_analysis(lead_id, analysis)

    except Exception as exc:
        logger.exception(
            "AI analysis generated but could not be saved for lead ID %s.",
            lead_id,
        )

        raise AnalysisPersistenceError(lead_id) from exc

    return {
        "lead_id": lead_id,
        "analysis_saved": True,
        "analysis": analysis,
        "error": None,
    }
