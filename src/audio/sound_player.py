"""
Play sounds from assets/sounds/.

Looping sounds use pygame.mixer.music (one at a time).
One-shot sounds use pygame.mixer.Sound on a channel.
"""

from pathlib import Path

import pygame

ROOT = Path(__file__).resolve().parent.parent.parent
SOUNDS_ROOT = ROOT / "assets" / "sounds"
_EXTENSIONS = (".mp3", ".wav", ".ogg")


class SoundPlayer:
    def __init__(self):
        self._looping_key = None
        self._one_shot_cache = {}

    def _resolve(self, category, name):
        """Return path for category/name or None if missing."""
        for ext in _EXTENSIONS:
            path = SOUNDS_ROOT / category / f"{name}{ext}"
            if path.exists():
                return path
        return None

    def play(self, category, name, *, loop=False, volume=0.7):
        """
        Play a sound. Use loop=True for ringtone/dial tone, False for short effects.
        category/name map to assets/sounds/<category>/<name>.mp3
        """
        path = self._resolve(category, name)
        if path is None:
            return
        volume = max(0.0, min(1.0, volume))
        key = f"{category}/{name}"

        if loop:
            self.stop()
            try:
                pygame.mixer.music.load(str(path))
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play(-1)
                self._looping_key = key
            except pygame.error:
                self._looping_key = None
        else:
            try:
                if key not in self._one_shot_cache:
                    self._one_shot_cache[key] = pygame.mixer.Sound(str(path))
                sound = self._one_shot_cache[key]
                sound.set_volume(volume)
                sound.play()
            except pygame.error:
                pass

    def stop(self):
        """Stop the current looping sound (music channel)."""
        if self._looping_key is not None:
            try:
                pygame.mixer.music.stop()
            except pygame.error:
                pass
            self._looping_key = None

    def stop_all(self):
        """Stop looping music and all active sound channels."""
        self.stop()
        try:
            pygame.mixer.stop()
        except pygame.error:
            pass