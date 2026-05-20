import pygame

from src.input import Action


class BaseScreen:
    manager = None  # set by ScreenRouter.register

    def __init__(self):
        self.name = None
        self.fonts = None
        self.menu = None

    def handle(self, action):
        if action == Action.UP:
            self.menu.move_up()
        elif action == Action.DOWN:
            self.menu.move_down()
        elif action == Action.SELECT:
            choice = self.menu.selection
            if choice == "back":
                self.manager.go_back()
            elif self.manager.has_screen(choice):
                self.manager.go_to(choice)

    def draw(self, surface):
        surface.fill((10, 12, 18))

        pygame.draw.rect(surface, (20, 24, 34), (0, 0, surface.get_width(), 28))
        os_label = self.fonts["small"].render("bugOS", True, (255, 255, 255))
        surface.blit(os_label, (8, 7))
        battery = self.fonts["small"].render("100%", True, (255, 255, 255))
        surface.blit(battery, (surface.get_width() - 8 - battery.get_width(), 7))

        title = self.fonts["large"].render(self.name, True, (255, 255, 255))
        surface.blit(title, (16, 48))

        self.menu.draw(surface)