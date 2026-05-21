from .base_screen import BaseScreen
from ..data_storing import load_contact_into
from src.input import Action


class IncomingCallScreen(BaseScreen):
    def __init__(self, fonts):
        super().__init__()
        self.fonts = fonts
        self.menu = None
        self.contact_id = None
        self.caller_name = "Unknown"
        self.photo = None
        self._selected = "accept"

    def load_contact(self, contact_id):
        load_contact_into(self, contact_id)

    def handle(self, action):
        if action in (Action.LEFT, Action.RIGHT):
            self._selected = "decline" if self._selected == "accept" else "accept"
        elif action == Action.SELECT:
            if self._selected == "accept":
                self.manager.call.answer()
            elif self._selected == "decline":
                self.manager.call.decline()

    def draw_content(self, surface):
        self.draw_caller_header(surface, "Incoming Call")
        self.draw_button(
            surface, 24, 188, 128, 36, "Accept", (40, 140, 80),
            selected=self._selected == "accept",
        )
        self.draw_button(
            surface, 168, 188, 128, 36, "Decline", (140, 50, 50),
            selected=self._selected == "decline",
        )