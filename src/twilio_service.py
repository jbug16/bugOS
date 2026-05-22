"""Twilio API wrapper for BugOS calls."""

import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

_TERMINAL_STATUSES = frozenset({
    "completed", "busy", "failed", "no-answer", "canceled",
})

_ANSWER_PRIOR_STATUSES = frozenset({"ringing", "initiated", "queued"})


class TwilioService:
    def __init__(self):
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.twilio_number = os.getenv("TWILIO_PHONE_NUMBER")

        if not all([self.account_sid, self.auth_token, self.twilio_number]):
            raise ValueError("Missing Twilio environment variables.")

        self.client = Client(self.account_sid, self.auth_token)

    def start_call(self, to_number):
        call = self.client.calls.create(
            to=to_number,
            from_=self.twilio_number,
            url="http://demo.twilio.com/docs/voice.xml"
        )
        return call.sid

    def fetch_call(self, call_sid):
        return self.client.calls(call_sid).fetch()

    def get_call_status(self, call_sid):
        return self.fetch_call(call_sid).status

    def is_call_ended(self, call):
        """True when the call (or all child legs) has ended."""
        if call.status in _TERMINAL_STATUSES:
            return True
        if call.status == "in-progress":
            children = self.client.calls.list(parent_call_sid=call.sid, limit=20)
            if children and all(c.status in _TERMINAL_STATUSES for c in children):
                return True
        return False

    def is_answered_transition(self, prior_status, current_status):
        """True only when the callee picked up (not a stray in-progress)."""
        return (
            current_status == "in-progress"
            and prior_status in _ANSWER_PRIOR_STATUSES
        )

    def end_call(self, call_sid):
        call = self.client.calls(call_sid).update(status="completed")
        return call.sid