# backend/services/notification_service.py
import datetime
import json
import os
import requests
from twilio.rest import Client

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "YOUR_TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "YOUR_TWILIO_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "+1234567890")

EMERGENCY_WEBHOOK_URL = os.getenv("EMERGENCY_WEBHOOK_URL", "https://example.com/api/v1/emergency-alerts")

class NotificationService:
    def __init__(self):
        self.twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN) if TWILIO_ACCOUNT_SID.startswith("AC") else None

    def send_sms(self, phone: str, message: str) -> bool:
        if not self.twilio_client:
            print(f"[SIMULATED SMS to {phone}]: {message}")
            return True
        try:
            res = self.twilio_client.messages.create(body=message, from_=TWILIO_PHONE_NUMBER, to=phone)
            print(f"[SMS SENT] SID: {res.sid}")
            return True
        except Exception as e:
            print(f"[SMS ERROR]: {e}")
            return False

    def trigger_agency_webhook(self, payload: dict):
        try:
            res = requests.post(EMERGENCY_WEBHOOK_URL, data=json.dumps(payload), headers={"Content-Type": "application/json"}, timeout=5)
            print(f"[WEBHOOK SENT] Status: {res.status_code}")
        except Exception as e:
            print(f"[WEBHOOK ERROR]: {e}")

    def notify_critical_event(self, region: str, risk_score: float, phone_list: list[str]):
        """Dispatches automated SMS and Webhooks if risk score reaches CRITICAL threshold."""
        if risk_score >= 0.75:
            message = (
                f"🚨 CRITICAL LANDSLIDE ALERT 🚨\n"
                f"Region: {region}\n"
                f"Risk Index: {int(risk_score * 100)}%\n"
                f"Action Required: Evacuate immediately via safe routes."
            )
            for phone in phone_list:
                self.send_sms(phone, message)

            webhook_payload = {
                "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                "severity": "CRITICAL",
                "region": region,
                "risk_score": risk_score
            }
            self.trigger_agency_webhook(webhook_payload)

# Global Instance
notification_service = NotificationService()