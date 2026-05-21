from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"

CONTACTS = {
    "john_pork": {
        "name": "John Pork",
        "photo": ASSETS / "john_pork.jpeg",
    },
}


def get_contact(contact_id):
    return CONTACTS.get(contact_id)