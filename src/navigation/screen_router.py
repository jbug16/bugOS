"""
Owns every screen and tracks which one is active.
"""


class ScreenRouter:
    def __init__(self):
        self._screens = {}
        self._current = None
        self._history = []

    def register(self, name, screen):
        screen.manager = self
        self._screens[name] = screen
        if self._current is None:
            self._current = name

    def has_screen(self, name):
        return name in self._screens

    def go_to(self, name):
        if name not in self._screens:
            print(f"No screen registered as {name!r}")
            return
        if self._current is not None and self._current != name:
            self._history.append(self._current)
        self._current = name
        self.current.menu.selected = 0 # make sure first item is selected

    def go_back(self):
        if self._history:
            self._current = self._history.pop()

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
