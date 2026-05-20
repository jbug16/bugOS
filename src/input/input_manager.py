"""
Translates raw input into abstract Actions.
"""

from enum import Enum, auto

import pygame


class Action(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    SELECT = auto()
    BACK = auto()
    CALL = auto()
    END = auto()
    QUIT = auto()  # window close / hard exit (dev convenience)


_KEY_MAP = {
    pygame.K_UP: Action.UP,
    pygame.K_w: Action.UP,
    pygame.K_DOWN: Action.DOWN,
    pygame.K_s: Action.DOWN,
    pygame.K_LEFT: Action.LEFT,
    pygame.K_a: Action.LEFT,
    pygame.K_RIGHT: Action.RIGHT,
    pygame.K_d: Action.RIGHT,
    pygame.K_RETURN: Action.SELECT,
    pygame.K_SPACE: Action.SELECT,
    pygame.K_ESCAPE: Action.BACK,
    pygame.K_BACKSPACE: Action.BACK,
    pygame.K_c: Action.CALL,
    pygame.K_x: Action.END,
}


class InputManager:
    def poll(self):
        """
        Yield an Action for each input event this frame.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                yield Action.QUIT
            elif event.type == pygame.KEYDOWN:
                action = _KEY_MAP.get(event.key)
                if action is not None:
                    yield action