
import json

from database.db import (
    get_recent_leads,
    update_lead_analysis
)

# Use the actual AI response received in our successful P-002 test.
analysis = {
    "category": "Healthcare Technology",
    "summary": (
        "The customer is seeking an automated appointment "
        "management system for Green Valley Healthcare clinic "
        "and requested details regarding features, pricing, "
        "and the implementation timeline."
    ),
    "intent": (
        "Evaluating and planning the implementation of an "
        "automated appointment management system by requesting "
        "feature details, pricing, and implementation timelines."
    ),
    "priority": "Hot",
    "reasoning": (
        "The customer explicitly requests pricing and an "
        "implementation timeline for an automated appointment "
        "management system, aligning with the pricing and "
        "implementation-focused priority criteria."
    ),
    "missing_information": [
        "Budget constraints",
        "Specific timeline or target launch date",
        "Clinic size, number of practitioners, or appointment volume",
        "Integration requirements with existing healthcare or EHR systems",
        "Decision-making role or purchasing authority of Sarah Johnson"
    ]
}

try:
    # Find the existing sample lead.
    leads = get_recent_leads()

    matching_leads = [
        lead for lead in leads
        if lead["customer_name"] == "Sarah Johnson"
        and lead["company"] == "Green Valley Healthcare"
    ]

    if not matching_leads:
        raise ValueError(
            "Sarah Johnson test lead was not found. "
            "No database record was updated."
        )

    lead = matching_leads[0]
    lead_id = lead["id"]

    print("Found test lead ID:", lead_id)

    # Save AI analysis against the existing lead.
    update_lead_analysis(lead_id, analysis)

    print("\nAI analysis saved successfully.")

    # Retrieve the updated lead.
    updated_leads = get_recent_leads()

    updated_lead = next(
        item for item in updated_leads
        if item["id"] == lead_id
    )

    print("\nDATABASE VERIFICATION")
    print("=" * 40)
    print("Lead ID:", updated_lead["id"])
    print("Customer:", updated_lead["customer_name"])
    print("Category:", updated_lead["category"])
    print("Priority:", updated_lead["priority"])
    print("Summary:", updated_lead["ai_summary"])
    print("Intent:", updated_lead["ai_intent"])
    print("Reasoning:", updated_lead["ai_reasoning"])

    print("\nMissing Information:")
    missing_items = json.loads(
        updated_lead["missing_information"]
    )

    for item in missing_items:
        print("-", item)

    print("\nSUCCESS: Database update and retrieval verified.")

except Exception as error:
    print("\nDATABASE TEST FAILED")
    print("Error type:", type(error).__name__)
    print("Error details:", str(error))
