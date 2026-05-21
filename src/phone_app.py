import pygame

from .call import CallManager
from .input import InputManager, Action
from .navigation import ScreenRouter
from .screens.incoming_call_screen import IncomingCallScreen
from .screens.ongoing_call_screen import OngoingCallScreen
from .screens.outgoing_call_screen import OutgoingCallScreen
from .data_storing import SettingsStore
from .screens.home_screen import HomeScreen
from .screens.settings_screen import SettingsScreen


class PhoneApp:
    WIDTH = 320
    HEIGHT = 240
    FPS = 30

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("bugOS")
        self.clock = pygame.time.Clock()
        self.running = True

        self.fonts = {
            "large": pygame.font.SysFont("arial", 24, bold=True),
            "medium": pygame.font.SysFont("arial", 18),
            "small": pygame.font.SysFont("arial", 14),
        }

        self.settings = SettingsStore()
        self.input = InputManager()
        self.router = ScreenRouter()
        self._register_screens()
        self.calls = CallManager(self.router, settings=self.settings)
        self.router.call = self.calls

        # test call
        self.calls.start_incoming(2398982770)

    def _register_screens(self):
        self.router.register("home", HomeScreen(self.fonts))
        self.router.register("settings", SettingsScreen(self.fonts, self.settings))
        self.router.register("incoming_call", IncomingCallScreen(self.fonts))
        self.router.register("ongoing_call", OngoingCallScreen(self.fonts))
        self.router.register("outgoing_call", OutgoingCallScreen(self.fonts))

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

        self.calls.shutdown()
        pygame.quit()