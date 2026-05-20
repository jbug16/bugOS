import pygame
from pathlib import Path

from .base_screen import BaseScreen
from ..contacts import get_contact
from src.input import Action


class IncomingCallScreen(BaseScreen):
    def __init__(self, fonts, contact_id="john_pork"):
        super().__init__()
        self.fonts = fonts
        self.menu = None

        contact = get_contact(contact_id)
        self.caller_name = contact["name"] if contact else "Unknown"
        photo_path = contact["photo"] if contact else None

        self.photo = None
        if photo_path and Path(photo_path).exists():
            img = pygame.image.load(str(photo_path))
            self.photo = pygame.transform.smoothscale(img, (72, 72))

        self._selected = "accept"

    def handle(self, action):
        if action in (Action.LEFT, Action.RIGHT):
            self._selected = "decline" if self._selected == "accept" else "accept"

    def draw(self, surface):
        w, h = surface.get_width(), surface.get_height()
        surface.fill((10, 12, 18))

        pygame.draw.rect(surface, (20, 24, 34), (0, 0, w, 28))
        os_label = self.fonts["small"].render("bugOS", True, (255, 255, 255))
        surface.blit(os_label, (8, 7))
        battery = self.fonts["small"].render("100%", True, (255, 255, 255))
        surface.blit(battery, (surface.get_width() - 8 - battery.get_width(), 7))

        title = self.fonts["medium"].render("Incoming Call", True, (200, 210, 230))
        surface.blit(title, (w // 2 - title.get_width() // 2, 36))

        name = self.fonts["large"].render(self.caller_name, True, (255, 255, 255))
        surface.blit(name, (w // 2 - name.get_width() // 2, 58))

        if self.photo:
            px = w // 2 - 36
            surface.blit(self.photo, (px, 96))

        self._draw_button(
            surface, 24, 188, 128, 36, "Accept", (40, 140, 80),
            self._selected == "accept",
        )
        self._draw_button(
            surface, 168, 188, 128, 36, "Decline", (140, 50, 50),
            self._selected == "decline",
        )

    def _draw_button(self, surface, x, y, bw, bh, label, color, selected):
        bg = color if selected else tuple(c // 2 for c in color)
        pygame.draw.rect(surface, bg, (x, y, bw, bh), border_radius=8)
        text = self.fonts["medium"].render(label, True, (255, 255, 255))
        surface.blit(text, (x + bw // 2 - text.get_width() // 2, y + 8))
