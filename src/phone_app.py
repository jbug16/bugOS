import pygame

from .input import InputManager, Action
from .navigation import ScreenRouter
from .settings_store import SettingsStore
from .screens.home_screen import HomeScreen
from .screens.settings_screen import SettingsScreen

class PhoneApp:
    WIDTH = 320
    HEIGHT = 240
    FPS = 30

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("bugOS")
        self.clock = pygame.time.Clock()
        self.running = True

        # Shared fonts so every screen has the same typography.
        self.fonts = {
            "large": pygame.font.SysFont("arial", 24, bold=True),
            "medium": pygame.font.SysFont("arial", 18),
            "small": pygame.font.SysFont("arial", 14),
        }

        self.settings = SettingsStore()
        self.input = InputManager()
        self.router = ScreenRouter()
        self._register_screens()

    def _register_screens(self):
        self.router.register("home", HomeScreen(self.fonts))
        self.router.register(
            "settings", SettingsScreen(self.fonts, self.settings)
        )
        self.router.go_to("home")

    def run(self):
        while self.running:
            for action in self.input.poll():
                if action == Action.QUIT:
                    self.running = False
                else:
                    self.router.handle(action)

            self.router.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(self.FPS)

        pygame.quit()
