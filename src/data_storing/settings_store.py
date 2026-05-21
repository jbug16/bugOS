import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULTS = {"volume": 70, "brightness": 80}
SETTINGS_PATH = ROOT / "data" / "settings.json"


def _clamp(value):
    return max(0, min(100, int(value)))


class SettingsStore:
    def __init__(self):
        self.values = DEFAULTS.copy()
        self._load()

    def _load(self):
        if not SETTINGS_PATH.exists():
            return
        try:
            data = json.loads(SETTINGS_PATH.read_text())
            for key in DEFAULTS:
                if key in data:
                    self.values[key] = _clamp(data[key])
        except (json.JSONDecodeError, OSError, TypeError, ValueError):
            pass

    def save(self):
        SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
        try:
            SETTINGS_PATH.write_text(
                json.dumps(self.values, indent=2) + "\n"
            )
        except OSError:
            pass

    def adjust(self, key, delta):
        if key not in self.values:
            return
        self.values[key] = _clamp(self.values[key] + delta)
        self.save()
