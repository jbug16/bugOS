from .base_screen import BaseScreen
from ..data_storing import load_contact_into
from src.input import Action


class OngoingCallScreen(BaseScreen):
    def __init__(self, fonts):
        super().__init__()
        self.fonts = fonts
        self.menu = None
        self.contact_id = None
        self.caller_name = "Unknown"
        self.photo = None
        self._selected = "end"

    def load_contact(self, contact_id):
        load_contact_into(self, contact_id)

    def handle(self, action):
        if action == Action.SELECT:
            self.manager.call.end()

    def draw_content(self, surface):
        self.draw_caller_header(surface, self.manager.call.format_call_timer())
        self.draw_button(
            surface, 96, 188, 128, 36, "End", (140, 50, 50),
            selected=True, dim_unselected=False,
        )