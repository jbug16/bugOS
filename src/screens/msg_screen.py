from .base_screen import BaseScreen
from ..ui.menu import Menu
from src.input import Action
from ..data_storing import list_contact_ids


class MsgScreen(BaseScreen):
    def __init__(self, fonts):
        super().__init__()
        self.fonts = fonts
        self.name = "Messages"
        self.menu = Menu(
            items=list_contact_ids() + ["back"],
            font=fonts["medium"],
        )

    def handle(self, action):
        choice = self.menu.selection

        if action == Action.SELECT:
            if choice == "back":
                self.manager.go_back()
                return

        if action == Action.UP:
            self.menu.move_up()
        elif action == Action.DOWN:
            self.menu.move_down()