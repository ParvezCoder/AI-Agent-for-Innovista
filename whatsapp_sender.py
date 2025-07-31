from agents import function_tool
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# ✅ Staff numbers list
STAFF_NUMBERS = [
    # "+923052887779",  # Staff 1
    "+923113536989",  # Staff 2
    # "+923212345678",  # Staff 3
]

@function_tool
def send_complaint_to_staff(name: str, complaint_type: str,company_name:str, complaint_detail: str) -> list:
    """
    Jese hi koi new complaint receive ho, ye function teen staff numbers par WhatsApp message bhejta hai.
    Message mein complainant ka naam, complaint type aur detail hoti hai.
    """
    instance_id = os.getenv("INSTANCE_ID")
    token = os.getenv("API_TOKEN")

    url = f"https://api.ultramsg.com/{instance_id}/messages/chat"

    # 📄 Message description
    message = f"""
📩 *New Complaint Received*
🏚  *Innovista AI Smart Agent*

👤 Name: {name}
⚙️ Type: {complaint_type}
✅ company name: {company_name}
📝 Detail: {complaint_detail}

🔔 Please take immediate action.
 Made by ❤ Muzaffar ALi.
    """.strip()

    # 📨 Send message to all staff
    results = []
    for number in STAFF_NUMBERS:
        payload = {
            "token": token,
            "to": number,
            "body": message
        }
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            results.append(f"✅ Message sent to {number}")
        else:
            results.append(f"❌ Failed for {number}: {response.text}")
    
    return results
