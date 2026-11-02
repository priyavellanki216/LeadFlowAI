
from modules.ai_service import analyze_lead

customer_name = "Sarah Johnson"
company = "Green Valley Healthcare"

enquiry = """
We are looking for an automated appointment management
system for our healthcare clinic. We would like to
understand the available features, pricing and
implementation timeline.
"""

try:
    result = analyze_lead(
        customer_name,
        company,
        enquiry
    )

    print("\nGEMINI LEAD ANALYSIS")
    print("=" * 45)
    print("Category:", result["category"])
    print("Summary:", result["summary"])
    print("Intent:", result["intent"])
    print("Priority:", result["priority"])
    print("Reasoning:", result["reasoning"])

    print("\nMissing Information:")
    for item in result["missing_information"]:
        print("-", item)

    print("\nAI analysis and validation successful.")

except Exception as error:
    print("\nAI analysis failed.")
    print("Error type:", type(error).__name__)
    print("Error details:", str(error))
