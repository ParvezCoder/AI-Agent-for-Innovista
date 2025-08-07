import requests
from agents import function_tool
#testing
@function_tool
def post_all_complaints_from_sheet(name: str, company_name: str, phone: str, complaint_type: str, description: str,status="In Process")-> str:
    """
    Posts a complaint entry to Google Sheet using a webhook (Google Apps Script or Pipedream).
    """

    url = "https://script.google.com/macros/s/AKfycbwULM0Pw-GfsuXIsrCs8JSfKF57OSJMuRmBx4P3j7H8sN5Ni9JF-YCtlofwWcA9VYlX6w/exec"  # <-- Replace with actual deployed Google Apps Script or Pipedream URL

    payload = {
        "name": name,
        "company_name": company_name,
        "phone": phone,
        "complaint_type": complaint_type,
        "description": description,
        "status": status,  # Automatically set when posted
        "auto_processed": True,
        "admin_remarks": ""     # Empty initially, admin will update later
    }
    

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return "✅ Complaint successfully submitted!"
    else:
        return f"❌ Failed to submit complaint. Status: {response.status_code}"

