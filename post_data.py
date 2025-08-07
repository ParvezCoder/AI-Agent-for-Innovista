import requests
from agents import function_tool
#testing
@function_tool
def post_all_complaints_from_sheet(name: str,company_name: str,phone: str,complaint_type: str,description: str):
    """
    Posts a complaint entry to Google Sheet using a webhook (Google Apps Script or Pipedream).
    """

    url = "https://script.google.com/macros/s/AKfycbwcg8icbzcpmnrsiqG_NuxbEZ2J7DRNlLVYBKcITH8_77Q4xP9LDUAsRL-j-iACv4vD/exec"  # <-- Replace with actual deployed Google Apps Script or Pipedream URL

    payload = {
        "name": name,
        "company_name": company_name,
        "phone": phone,
        "complaint_type": complaint_type,
        "description": description,
        # "status": status,  # Automatically set when posted
        # "auto_processed": True,
        # "admin_remarks": ""     # Empty initially, admin will update later
    }
    

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return "✅ Complaint successfully submitted!"
    else:
        return f"❌ Failed to submit complaint. Status: {response.status_code}"

