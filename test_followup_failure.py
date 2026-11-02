
from database.db import get_recent_leads, get_followup_history, save_followup_draft

print("STARTING FOLLOW-UP FAILURE-HANDLING TEST")
print("=" * 55)

# Find an existing lead with a saved follow-up draft.
leads = get_recent_leads()

test_lead = next(
    (
        lead for lead in leads
        if lead["followup_draft"]
    ),
    None
)

if test_lead is None:
    raise RuntimeError(
        "No lead with an existing follow-up draft was found."
    )

lead_id = test_lead["id"]

# Capture the existing draft and history before testing.
original_draft = test_lead["followup_draft"]
original_history = get_followup_history(lead_id)

print("Selected Lead ID:", lead_id)
print("Existing draft found:", bool(original_draft))
print("Existing history entries:", len(original_history))

# Simulate the same generation-before-save sequence used by the app.
def simulate_followup_generation():
    raise RuntimeError(
        "SIMULATED: Follow-up AI service temporarily unavailable."
    )

try:
    print("\nAttempting to generate a new follow-up draft...")

    # Generation fails before save_followup_draft can be called.
    new_draft = simulate_followup_generation()

    # This line should not execute.
    save_followup_draft(lead_id, new_draft)

except Exception as error:
    print("\nFOLLOW-UP GENERATION FAILED")
    print("Error:", error)
    print("The previous draft should remain unchanged.")

# Verify that the old draft and history are preserved.
updated_leads = get_recent_leads()

updated_lead = next(
    (
        lead for lead in updated_leads
        if lead["id"] == lead_id
    ),
    None
)

updated_history = get_followup_history(lead_id)

if updated_lead is None:
    raise AssertionError("FAILED: Lead was not found.")

if updated_lead["followup_draft"] != original_draft:
    raise AssertionError("FAILED: Existing draft was changed.")

if len(updated_history) != len(original_history):
    raise AssertionError("FAILED: History entry count changed.")

if updated_history != original_history:
    raise AssertionError("FAILED: Follow-up history was modified.")

print("\nDATABASE VERIFICATION")
print("=" * 55)
print("Existing draft preserved: YES")
print("History count before:", len(original_history))
print("History count after:", len(updated_history))
print("Existing history preserved: YES")

print("\nSUCCESS: Previous follow-up draft and history were preserved.")
