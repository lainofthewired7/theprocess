"""Firestore connection. Import `db` (or use get_db in api/deps.py) anywhere you need it."""
import firebase_admin
from firebase_admin import credentials, firestore

from app.config import FIREBASE_KEY_PATH


def _init_firebase() -> None:
    if firebase_admin._apps:  # already initialized (e.g. uvicorn --reload)
        return
    if not FIREBASE_KEY_PATH.exists():
        raise RuntimeError(
            f"Firebase key not found at {FIREBASE_KEY_PATH}. Download your own from "
            "Firebase Console > Project settings > Service accounts and save it there, "
            "or set GOOGLE_APPLICATION_CREDENTIALS in theprocess/.env."
        )
    firebase_admin.initialize_app(credentials.Certificate(FIREBASE_KEY_PATH))


_init_firebase()
db = firestore.client()
