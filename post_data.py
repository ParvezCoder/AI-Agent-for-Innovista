import requests
from agents import function_tool
# testing remove
@function_tool
def post_all_complaints_from_sheet(name: str,company_name: str,phone: str,complaint_type: str,description: str,status: str = "Pending"):
    """
    Posts a complaint entry to Google Sheet using a webhook (Google Apps Script or Pipedream).
    """

    url = "https://script.google.com/macros/s/AKfycbxv9tBKo1C8oBOS8A5EnIkFF642weWjL7KFbMxbbmZVoEhwi6NQuMnT1-eFXPJmklbpFQ/exec"  # <-- Replace with actual deployed Google Apps Script or Pipedream URL

    payload = {
        "name": name,
        "company_name": company_name,
        "phone": phone,
        "complaint_type": complaint_type,
        "description": description,
        "status": status,  
       
    }
    
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return "✅ Complaint successfully submitted!"
    else:
        return f"❌ Failed to submit complaint. Status: {response.status_code}"
