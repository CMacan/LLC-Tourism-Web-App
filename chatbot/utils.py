import requests
from django.conf import settings

def send_message_to_gemini(message, conversation_id=None):
    url = settings.GEMINI_API_URL
    headers = {
        "Authorization": f"Bearer {settings.GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "message": message,
        "conversation_id": conversation_id  # Optional: for maintaining context
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to connect to Gemini API"}
