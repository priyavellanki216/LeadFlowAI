
from modules.ai_service import generate_followup_draft

customer_name = "Sarah Johnson"
company = "Green Valley Healthcare"

enquiry = """
We are looking for an automated appointment management
system for our healthcare clinic. We would like to
understand the available features, pricing and
implementation timeline.
"""

ai_summary = (
    "The customer is seeking an automated appointment "
    "management system for Green Valley Healthcare clinic "
    "and requested details regarding features, pricing, "
    "and the implementation timeline."
)

intent = (
    "Evaluating and planning the implementation of an "
    "automated appointment management system by requesting "
    "feature details, pricing, and implementation timelines."
)

priority = "Hot"

try:

    draft = generate_followup_draft(
        customer_name,
        company,
        enquiry,
        ai_summary,
        intent,
        priority
    )

    print("\nGENERATED FOLLOW-UP EMAIL")
    print("=" * 50)
    print(draft)

    print("\nSUCCESS: Follow-up draft generated successfully.")

except Exception as error:

    print("\nFOLLOW-UP GENERATION FAILED")
    print("Error type:", type(error).__name__)
    print("Error details:", str(error))
