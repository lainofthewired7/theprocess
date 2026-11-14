"""Firestore logic for items. Routers call these functions; only services touch Firestore.

Each function returns plain data (or None when not found) and knows nothing about HTTP.
"""
from datetime import datetime, timezone
from typing import Optional

from google.cloud.firestore import Client, Query

from app.schemas.item import Item, ItemCreate, ItemUpdate

COLLECTION = "items"


def _to_item(doc) -> Item:
    return Item(id=doc.id, **doc.to_dict())


def create_item(db: Client, item: ItemCreate) -> Item:
    doc_ref = db.collection(COLLECTION).document()  # auto-generated ID
    data = {**item.model_dump(), "created_at": datetime.now(timezone.utc)}
    doc_ref.set(data)
    return Item(id=doc_ref.id, **data)


def list_items(db: Client, limit: int) -> list[Item]:
    docs = (
        db.collection(COLLECTION)
        .order_by("created_at", direction=Query.DESCENDING)
        .limit(limit)
        .stream()
    )
    return [_to_item(doc) for doc in docs]


def get_item(db: Client, item_id: str) -> Optional[Item]:
    doc = db.collection(COLLECTION).document(item_id).get()
    return _to_item(doc) if doc.exists else None


def update_item(db: Client, item_id: str, changes: ItemUpdate) -> Optional[Item]:
    doc_ref = db.collection(COLLECTION).document(item_id)
    if not doc_ref.get().exists:
        return None
    updates = changes.model_dump(exclude_unset=True)  # only fields that were sent
    if updates:
        doc_ref.update(updates)
    return _to_item(doc_ref.get())


def delete_item(db: Client, item_id: str) -> bool:
    doc_ref = db.collection(COLLECTION).document(item_id)
    if not doc_ref.get().exists:
        return False
    doc_ref.delete()
    return True
