"""Call state, sounds, and screen transitions for incoming/ongoing calls."""

import time
from enum import Enum, auto

from src.audio import SoundPlayer
from src.data_storing import get_contact_phone_e164
from src.twilio_service import TwilioService

class CallState(Enum):
    IDLE = auto()
    RINGING = auto()
    ACTIVE = auto()


class CallManager:
    def __init__(self, router, settings=None):
        self.router = router
        self.settings = settings
        self.state = CallState.IDLE
        self.caller_id = None
        self._call_started_at = None
        self._audio = SoundPlayer()

        # twilio - VoIP service
        self._twilio = TwilioService()
        self.current_call_sid = None
        self._waiting_for_answer = False
        self._last_status_poll = 0.0
        self._prior_call_status = None

    def format_call_timer(self):
        if self._call_started_at is None:
            return "0:00"
        elapsed = int(time.monotonic() - self._call_started_at)
        mins, secs = divmod(elapsed, 60)
        return f"{mins}:{secs:02d}"

    def _volume(self):
        if self.settings is not None:
            return self.settings.values.get("volume", 70) / 100
        return 0.7

    def _screen(self, name):
        return self.router._screens.get(name)

    def _load_caller(self, screen_name, contact_id):
        screen = self._screen(screen_name)
        if screen is not None and hasattr(screen, "load_contact"):
            screen.load_contact(contact_id)

    def start_incoming(self, contact_id, *, call_sid=None):
        self.caller_id = contact_id
        self._call_started_at = None
        self.current_call_sid = call_sid
        self._last_status_poll = 0.0
        self.state = CallState.RINGING
        self._audio.play("call", "ringtone", loop=True, volume=self._volume())
        self._load_caller("incoming_call", contact_id)
        self.router.go_to("incoming_call")

    def start_outgoing(self, contact_id):
        self.caller_id = contact_id
        self._call_started_at = None
        self._waiting_for_answer = False
        self._prior_call_status = None
        self.state = CallState.ACTIVE

        self._load_caller("outgoing_call", contact_id)
        self.router.go_to("outgoing_call")

        self._audio.play("call", "dialing", loop=True, volume=self._volume())

        phone_number = get_contact_phone_e164(contact_id)
        if not phone_number:
            print(f"Call failed: no phone number for {contact_id!r}")
            self.current_call_sid = None
            self.end()
            return

        try:
            self.current_call_sid = self._twilio.start_call(phone_number)
            self._waiting_for_answer = True
            self._last_status_poll = 0.0
            print(f"Started Twilio call: {self.current_call_sid}")
        except Exception as e:
            print(f"Call failed: {e}")
            self.current_call_sid = None
            self.end()

    def update(self):
        """Poll Twilio while a call SID is active (ringing, dialing, or ongoing)."""
        if not self.current_call_sid:
            return

        poll_interval = 0.5 if self._waiting_for_answer else 1.0
        now = time.monotonic()
        if now - self._last_status_poll < poll_interval:
            return
        self._last_status_poll = now

        try:
            call = self._twilio.fetch_call(self.current_call_sid)
            status = call.status
        except Exception as e:
            print(f"Could not check call status: {e}")
            return

        if self._twilio.is_call_ended(call):
            if self.state == CallState.RINGING:
                print("Caller hung up")
                self._remote_ended_before_answer()
            elif self._waiting_for_answer:
                print(f"Call not answered: {status}")
                self.end(notify_twilio=False)
            else:
                print("Call ended remotely")
                self.end(notify_twilio=False)
            return

        if (
            self._waiting_for_answer
            and self.router._current == "outgoing_call"
            and self._twilio.is_answered_transition(self._prior_call_status, status)
        ):
            self._on_remote_answered()

        self._prior_call_status = status

    def _remote_ended_before_answer(self):
        self._waiting_for_answer = False
        self._audio.stop()
        self.current_call_sid = None
        self.caller_id = None
        self._call_started_at = None
        self.state = CallState.IDLE
        self.router.go_home()

    def _on_remote_answered(self):
        self._waiting_for_answer = False
        self._prior_call_status = None
        self._audio.stop()
        self._call_started_at = time.monotonic()
        self._load_caller("ongoing_call", self.caller_id)
        self.router.go_to("ongoing_call")

    def answer(self):
        if self.state != CallState.RINGING or not self.caller_id:
            return
        self._audio.stop()
        self.state = CallState.ACTIVE
        self._call_started_at = time.monotonic()
        self._load_caller("ongoing_call", self.caller_id)
        self.router.go_to("ongoing_call")

    def decline(self):
        self._waiting_for_answer = False
        self._audio.stop()
        if self.current_call_sid:
            try:
                self._twilio.end_call(self.current_call_sid)
            except Exception as e:
                print(f"Could not end Twilio call: {e}")
        self.current_call_sid = None
        self.caller_id = None
        self._call_started_at = None
        self.state = CallState.IDLE
        self.router.go_home()

    def end(self, *, notify_twilio=True):
        self._waiting_for_answer = False
        self._audio.stop()

        if notify_twilio and self.current_call_sid:
            try:
                self._twilio.end_call(self.current_call_sid)
                print(f"Ended Twilio call: {self.current_call_sid}")
            except Exception as e:
                print(f"Could not end Twilio call: {e}")

        self.current_call_sid = None
        self.caller_id = None
        self._call_started_at = None
        self.state = CallState.IDLE

        self._audio.play("call", "end_call", loop=False, volume=self._volume())
        self.router.go_to("call")

    def shutdown(self):
        self._audio.stop_all()