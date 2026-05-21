"""Call state, sounds, and screen transitions for incoming/ongoing calls."""

import time
from enum import Enum, auto

from src.audio import SoundPlayer


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

    def start_incoming(self, contact_id):
        self.caller_id = contact_id
        self._call_started_at = None
        self.state = CallState.RINGING
        self._audio.play("call", "ringtone", loop=True, volume=self._volume())
        self._load_caller("incoming_call", contact_id)
        self.router.go_to("incoming_call")

    def start_outgoing(self, contact_id):
        self.caller_id = contact_id
        self._call_started_at = None
        self.state = CallState.ACTIVE
        self._audio.play("call", "dialing", loop=True, volume=self._volume())
        self._load_caller("outgoing_call", contact_id)
        self.router.go_to("outgoing_call")

    def answer(self):
        if self.state != CallState.RINGING or not self.caller_id:
            return
        self._audio.stop()
        self.state = CallState.ACTIVE
        self._call_started_at = time.monotonic()
        self._load_caller("ongoing_call", self.caller_id)
        self.router.go_to("ongoing_call")

    def decline(self):
        self._audio.stop()
        self.caller_id = None
        self._call_started_at = None
        self.state = CallState.IDLE
        self.router.go_home()

    def end(self):
        self._audio.stop()
        self.caller_id = None
        self._call_started_at = None
        self.state = CallState.IDLE
        self._audio.play("call", "end_call", loop=False, volume=self._volume())
        self.router.go_home()

    def shutdown(self):
        self._audio.stop_all()