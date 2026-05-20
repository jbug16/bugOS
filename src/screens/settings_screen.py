from .base_screen import BaseScreen
from ..ui.menu import Menu


class SettingsScreen(BaseScreen):
    def __init__(self, fonts):
        super().__init__()
        self.fonts = fonts
        self.name = "Settings"
        self.menu = Menu(
            items=["volume", "brightness", "back"],
            font=fonts["medium"],
        )