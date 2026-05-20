"""
Reusable Menu widget: a vertical list of items with a selection cursor.
"""

import pygame


def _format_label(route_key: str) -> str:
    return route_key.replace("_", " ").title()

class Menu:
    def __init__(self, items, font, *, x=16, y=92, width=208,
                 row_height=35, card_height=30):
        if not items:
            raise ValueError("Menu needs at least one item")
        self.items = list(items)
        self.font = font
        self.selected = 0

        self.x = x
        self.y = y
        self.width = width
        self.row_height = row_height
        self.card_height = card_height

    @property
    def selection(self):
        return self.items[self.selected]

    def reset_selection(self):
        self.selected = 0

    def move_up(self):
        self.selected = (self.selected - 1) % len(self.items)

    def move_down(self):
        self.selected = (self.selected + 1) % len(self.items)

    def draw(self, surface):
        for i, item in enumerate(self.items):
            row_y = self.y + i * self.row_height

            if i == self.selected:
                bg = (70, 90, 140)
                fg = (255, 255, 255)
            else:
                bg = (28, 32, 44)
                fg = (190, 195, 210)

            pygame.draw.rect(
                surface, bg,
                (self.x, row_y, self.width, self.card_height),
                border_radius=8,
            )
            label = self.font.render(_format_label(item), True, fg)
            surface.blit(label, (self.x + 14, row_y + 6))
