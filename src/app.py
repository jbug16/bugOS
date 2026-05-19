"""
TODO:
- Create the main PhoneApp class.
- Start and stop the app loop.
- Hold the current screen/app state.
- Coordinate input, menus, and screen drawing.
- Later: switch between Contacts, Messages, Settings, and Call screens.
"""

import pygame

class PhoneApp:
    def __init__(self):
        pygame.init()

        # window size
        self.WIDTH = 240
        self.HEIGHT = 320
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        # window name
        pygame.display.set_caption("bugOS")

        # phone is on
        self.clock = pygame.time.Clock()
        self.running = True

        # selectable options
        self.menu_items = ["Call", "Contacts", "Messages", "Settings"]
        self.selected = 0

        # fonts
        self.font_large = pygame.font.SysFont("arial", 24, bold=True)
        self.font_medium = pygame.font.SysFont("arial", 18)
        self.font_small = pygame.font.SysFont("arial", 14)

    def draw_text(self, text, font, x, y, color=(255, 255, 255)):
        surface = font.render(text, True, color)
        self.screen.blit(surface, (x, y))

    def draw(self):
        self.screen.fill((10, 12, 18))

        # top status bar
        pygame.draw.rect(self.screen, (20, 24, 34), (0, 0, self.WIDTH, 28))
        self.draw_text("bugOS", self.font_small, 8, 7)

        # title
        self.draw_text("Home", self.font_large, 16, 48)

        # draw menu cards
        start_y = 92
        card_h = 42

        for i, item in enumerate(self.menu_items):
            y = start_y + i * 50

            if i == self.selected:
                color = (70, 90, 140)
                text_color = (255, 255, 255)
            else:
                color = (28, 32, 44)
                text_color = (190, 195, 210)

            pygame.draw.rect(self.screen, color, (16, y, 208, card_h), border_radius=8)
            self.draw_text(item, self.font_medium, 30, y + 11, text_color)

        # footer
        pygame.draw.rect(self.screen, (20, 24, 34), (0, 292, self.WIDTH, 28))
        self.draw_text("↑↓ Move   Enter Select", self.font_small, 32, 299)

        pygame.display.flip()

    def handle_keydown(self, key):
        # up arrow
        if key == pygame.K_UP or key == pygame.K_w:
            self.selected = (self.selected - 1) % len(self.menu_items)

        # down arrow
        elif key == pygame.K_DOWN or key == pygame.K_s:
            self.selected = (self.selected + 1) % len(self.menu_items)

        # enter
        elif key == pygame.K_RETURN:
            print(f"Selected: {self.menu_items[self.selected]}")

        # esc
        elif key == pygame.K_ESCAPE or key == pygame.K_q:
            self.running = False

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.KEYDOWN:
                    self.handle_keydown(event.key)

            self.draw()
            self.clock.tick(30)

        pygame.quit()