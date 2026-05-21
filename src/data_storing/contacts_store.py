import json
from pathlib import Path

import pygame

ROOT = Path(__file__).resolve().parent.parent.parent
CONTACT_IMAGES = ROOT / "assets" / "images" / "contacts"
CONTACTS_PATH = ROOT / "data" / "contacts.json"
UNKNOWN_PHOTO = CONTACT_IMAGES / "unknown.jpg"

_contacts = {}


def format_phone(value):
    """Format a phone number for display; returns original string if not numeric."""
    digits = "".join(c for c in str(value) if c.isdigit())
    if not digits:
        return str(value)
    if len(digits) == 11:
        return f"+{digits[0]} ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    return "Unknown"


def _load_contacts():
    global _contacts
    if not CONTACTS_PATH.exists():
        _contacts = {}
        return
    try:
        raw = json.loads(CONTACTS_PATH.read_text())
    except (json.JSONDecodeError, OSError):
        _contacts = {}
        return

    loaded = {}
    for contact_id, entry in raw.items():
        if not isinstance(entry, dict):
            continue
        name = entry.get("name", contact_id)
        photo_file = entry.get("photo")
        photo = CONTACT_IMAGES / photo_file if photo_file else None
        number = entry.get("number")
        loaded[contact_id] = {"name": name, "number": number, "photo": photo}
    _contacts = loaded


def get_contact(contact_id):
    if not _contacts:
        _load_contacts()
    return _contacts.get(contact_id)


def get_contact_by_number(number):
    """Find a contact whose stored number matches (int or string)."""
    if not _contacts:
        _load_contacts()
    digits = "".join(c for c in str(number) if c.isdigit())
    if not digits:
        return None
    target = int(digits) if digits.isdigit() else None
    for entry in _contacts.values():
        stored = entry.get("number")
        if stored is None:
            continue
        stored_digits = "".join(c for c in str(stored) if c.isdigit())
        if stored_digits == digits or (target is not None and stored == target):
            return entry
    return None


def load_contact_into(screen, contact_id):
    """Update a call screen's name and photo from a contact id or phone number."""
    screen.contact_id = contact_id
    contact = get_contact(contact_id)
    if contact is None:
        contact = get_contact_by_number(contact_id)

    if contact:
        screen.caller_name = contact["name"]
        photo_path = contact["photo"]
    else:
        screen.caller_name = format_phone(contact_id)
        photo_path = UNKNOWN_PHOTO if UNKNOWN_PHOTO.exists() else None

    screen.photo = None
    if photo_path and Path(photo_path).exists():
        img = pygame.image.load(str(photo_path))
        screen.photo = pygame.transform.smoothscale(img, (72, 72))


_load_contacts()