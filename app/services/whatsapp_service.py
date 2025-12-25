# app/services/whatsapp_service.py

import requests
import os

class WhatsAppService:
    def __init__(self):
        self.token = os.getenv("WHATSAPP_ACCESS_TOKEN")
        self.phone_id = os.getenv("PHONE_NUMBER_ID")
        self.version = "v18.0"
        self.url = f"https://graph.facebook.com/{self.version}/{self.phone_id}/messages"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def send_text_message(self, to, text):
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {"body": text}
        }
        return requests.post(self.url, json=payload, headers=self.headers)

    def send_buttons(self, to, text, buttons):
        format_buttons = [{"type": "reply", "reply": {"id": i, "title": t}} for i, t in buttons]
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {"text": text},
                "action": {"buttons": format_buttons}
            }
        }
        return requests.post(self.url, json=payload, headers=self.headers)