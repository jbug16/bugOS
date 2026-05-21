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

    def draw_status_bar(self, surface):
        w = surface.get_width()
        pygame.draw.rect(surface, (20, 24, 34), (0, 0, w, 28))
        os_label = self.fonts["small"].render("bugOS", True, (255, 255, 255))
        surface.blit(os_label, (8, 7))
        battery = self.fonts["small"].render("100%", True, (255, 255, 255))
        surface.blit(battery, (w - 8 - battery.get_width(), 7))

    def draw_background(self, surface):
        surface.fill((10, 12, 18))
        self.draw_status_bar(surface)

    def draw_content(self, surface):
        if self.name:
            title = self.fonts["large"].render(self.name, True, (255, 255, 255))
            surface.blit(title, (16, 48))
        if self.menu is not None:
            self.menu.draw(surface)

    def draw_caller_header(self, surface, subtitle):
        w = surface.get_width()
        title = self.fonts["medium"].render(subtitle, True, (200, 210, 230))
        surface.blit(title, (w // 2 - title.get_width() // 2, 36))
        name = self.fonts["large"].render(self.caller_name, True, (255, 255, 255))
        surface.blit(name, (w // 2 - name.get_width() // 2, 58))
        if self.photo:
            surface.blit(self.photo, (w // 2 - 36, 96))

    def draw_button(self, surface, x, y, bw, bh, label, color, *,
                    selected=True, dim_unselected=True):
        if dim_unselected and not selected:
            bg = tuple(c // 2 for c in color)
        else:
            bg = color
        pygame.draw.rect(surface, bg, (x, y, bw, bh), border_radius=8)
        text = self.fonts["medium"].render(label, True, (255, 255, 255))
        surface.blit(text, (x + bw // 2 - text.get_width() // 2, y + 8))

    def draw(self, surface):
        self.draw_background(surface)
        self.draw_content(surface)