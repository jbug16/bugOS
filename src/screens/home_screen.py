from .base_screen import BaseScreen
from ..ui.menu import Menu


class HomeScreen(BaseScreen):
    def __init__(self, fonts):
        super().__init__()
        self.fonts = fonts
        self.name = "Home"
        self.menu = Menu(
            items=["call", "messages", "contacts", "settings"],
            font=fonts["medium"],
        )