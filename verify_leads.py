
from database.db import get_recent_leads

leads = get_recent_leads()

print("Total saved leads:", len(leads))

for lead in leads:
    print("\nLead ID:", lead["id"])
    print("Customer:", lead["customer_name"])
    print("Email:", lead["email"])
    print("Company:", lead["company"])
    print("Enquiry:", lead["enquiry"])
