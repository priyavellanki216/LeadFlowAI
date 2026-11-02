
from database.db import (
    initialize_db,
    get_recent_leads,
    save_followup_draft,
    get_followup_history
)

# Make sure database tables are initialized
initialize_db()

# Retrieve existing leads
leads = get_recent_leads()

if not leads:
    print("No leads found. Submit a lead through the application first.")

else:
    # Use the most recent lead
    lead = leads[0]

    lead_id = lead["id"]

    print(f"Testing database storage for Lead ID: {lead_id}")

    test_draft = """
Subject: Following Up on Your Enquiry

Hi Customer,

Thank you for sharing your enquiry with us.
We would be happy to understand your requirements
and discuss the relevant next steps.

Best regards,
LeadFlow AI Team
"""

    try:
        # Save the follow-up draft
        save_followup_draft(lead_id, test_draft)

        print("\nSUCCESS: Follow-up draft saved.")

        # Retrieve follow-up history
        history = get_followup_history(lead_id)

        print("\nFOLLOW-UP HISTORY")
        print("=" * 50)

        for item in history:
            print(f"History ID: {item['id']}")
            print(f"Lead ID: {item['lead_id']}")
            print(f"Action: {item['action']}")
            print(f"Created At: {item['created_at']}")
            print("Draft:")
            print(item["draft"])
            print("-" * 50)

        if history and history[0]["draft"].strip() == test_draft.strip():
            print("\nSUCCESS: Database save and retrieval verified.")
        else:
            print("\nERROR: Saved draft does not match retrieved draft.")

    except Exception as error:
        print("\nDATABASE TEST FAILED")
        print("Error type:", type(error).__name__)
        print("Error details:", str(error))
