from modules.ai_service import get_gemini_client

client = get_gemini_client()

try:
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents="Reply with exactly: LeadFlow AI alternative model test successful."
    )

    print("\nALTERNATIVE MODEL RESPONSE")
    print("=" * 45)
    print(response.text)
    print("\nSUCCESS: Alternative model is responding.")

except Exception as error:
    print("\nALTERNATIVE MODEL TEST FAILED")
    print("Error type:", type(error).__name__)
    print("Error details:", str(error))