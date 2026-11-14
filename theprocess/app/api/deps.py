"""Shared FastAPI dependencies.

Endpoints take `db: Client = Depends(get_db)` instead of importing db directly,
so tests can swap in a fake database with app.dependency_overrides.
Later, a get_current_user dependency (verifying Firebase ID tokens) belongs here too.
"""
from google.cloud.firestore import Client

from app.database import db


def get_db() -> Client:
    return db
