
import os
from dotenv import load_dotenv
from google import genai

# Load credentials from the .env file
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: Gemini API key was not detected.")
    raise SystemExit(1)

try:
    # Create Gemini client
    client = genai.Client(api_key=api_key)

    print("Gemini API key detected.")
    print("Sending test request to Gemini...")

    # Test prompt
    prompt = """
    You are an AI assistant for a business lead management system.

    Reply with exactly:
    Gemini connection successful. LeadFlow AI is ready.
    """

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    if response.text:
        print("\nGemini response:")
        print(response.text)
        print("\nSUCCESS: Gemini API connection verified.")
    else:
        print("No text response received. Please investigate.")

except Exception as error:
    print("\nGemini API request failed.")
    print("Error type:", type(error).__name__)
    print("Error details:", str(error))
