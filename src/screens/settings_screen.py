from .base_screen import BaseScreen
from ..ui.menu import Menu
from src.input import Action

_ADJUSTABLE = frozenset({"volume", "brightness"})
_STEP = 5


class SettingsScreen(BaseScreen):
    def __init__(self, fonts, settings):
        super().__init__()
        self.fonts = fonts
        self.settings = settings
        self.name = "Settings"
        self.menu = Menu(
            items=["volume", "brightness", "back"],
            font=fonts["medium"],
            values=settings.values,
        )

    def handle(self, action):
        choice = self.menu.selection

        if choice in _ADJUSTABLE and action in (Action.LEFT, Action.RIGHT):
            delta = -_STEP if action == Action.LEFT else _STEP
            self.settings.adjust(choice, delta)
            return

        if action == Action.SELECT and choice == "back":
            self.manager.go_back()
            return

        if action == Action.UP:
            self.menu.move_up()
        elif action == Action.DOWN:
            self.menu.move_down()