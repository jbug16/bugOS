"""
Owns every screen and tracks which one is active.
"""

_CALL_FLOW = frozenset({"incoming_call", "outgoing_call", "ongoing_call"})


class ScreenRouter:
    def __init__(self):
        self._screens = {}
        self._current = None
        self._history = []
        self.call = None

    def register(self, name, screen):
        screen.manager = self
        self._screens[name] = screen
        if self._current is None:
            self._current = name

    def has_screen(self, name):
        return name in self._screens

    def _push_history(self, name):
        if name and (not self._history or self._history[-1] != name):
            self._history.append(name)

    def go_to(self, name):
        if name not in self._screens:
            print(f"No screen registered as {name!r}")
            return
        if self._current is not None and self._current != name:
            if self._history and self._history[-1] == name:
                self._history.pop()
            elif name in _CALL_FLOW:
                if self._current == "call":
                    self._push_history("call")
                elif self._current not in _CALL_FLOW:
                    self._push_history(self._current)
            elif self._current not in _CALL_FLOW:
                self._push_history(self._current)
        self._current = name
        menu = getattr(self.current, "menu", None)
        if menu is not None:
            menu.reset_selection()

    def go_home(self):
        self._history.clear()
        self._current = "home"
        menu = getattr(self.current, "menu", None)
        if menu is not None:
            menu.reset_selection()

    def go_back(self):
        while self._history and self._history[-1] in _CALL_FLOW:
            self._history.pop()
        if self._history:
            self._current = self._history.pop()
            menu = getattr(self.current, "menu", None)
            if menu is not None:
                menu.reset_selection()

    @property
    def current(self):
        if self._current is None:
            return None
        return self._screens[self._current]

    def handle(self, action):
        screen = self.current
        if screen is not None:
            screen.handle(action)

    def draw(self, surface):
        screen = self.current
        if screen is not None:
            screen.draw(surface)
