
from database.db import save_lead, get_recent_leads

print("STARTING AI FAILURE-HANDLING TEST")
print("=" * 50)

# Test customer information
customer_name = "Failure Test Customer"
email = "failure.test@example.com"
company = "Test Technologies"
enquiry = "We are interested in automating our business workflow."

try:
    # STEP 1: Save the lead before AI analysis.
    lead_id = save_lead(
        customer_name,
        email,
        company,
        enquiry
    )

    print(f"SUCCESS: Lead saved with ID: {lead_id}")

    # STEP 2: Simulate a Gemini service failure.
    try:
        raise RuntimeError(
            "SIMULATED: Gemini service temporarily unavailable."
        )

    except Exception as error:
        print("\nAI ANALYSIS FAILED")
        print(f"Error: {error}")
        print("The saved lead should remain in the database.")

    # STEP 3: Verify that the lead still exists.
    leads = get_recent_leads()

    saved_lead = next(
        (
            lead for lead in leads
            if lead["id"] == lead_id
        ),
        None
    )

    if saved_lead is None:
        raise AssertionError(
            "FAILED: Saved lead was not found."
        )

    if saved_lead["customer_name"] != customer_name:
        raise AssertionError(
            "FAILED: Customer information does not match."
        )

    print("\nDATABASE VERIFICATION")
    print("=" * 50)
    print("Lead ID:", saved_lead["id"])
    print("Customer:", saved_lead["customer_name"])
    print("Email:", saved_lead["email"])
    print("Company:", saved_lead["company"])
    print("Enquiry:", saved_lead["enquiry"])

    print("\nSUCCESS: Lead was preserved after simulated AI failure.")

except Exception as error:
    print("\nTEST FAILED")
    print("Error type:", type(error).__name__)
    print("Error details:", str(error))
