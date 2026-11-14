"""Test setup: runs the API against an in-memory fake Firestore (no key, no real data touched)."""
import sys
import types
import uuid

import pytest

# Stop app.database from connecting to real Firebase when the app is imported.
_fake_database = types.ModuleType("app.database")
_fake_database.db = None
sys.modules["app.database"] = _fake_database

from fastapi.testclient import TestClient  # noqa: E402

from app.api.deps import get_db  # noqa: E402
from app.main import app  # noqa: E402


class FakeDoc:
    def __init__(self, store, doc_id):
        self.store, self.id = store, doc_id

    @property
    def exists(self):
        return self.id in self.store

    def get(self):
        return self

    def to_dict(self):
        return dict(self.store[self.id])

    def set(self, data):
        self.store[self.id] = dict(data)

    def update(self, data):
        self.store[self.id].update(data)

    def delete(self):
        del self.store[self.id]


class FakeQuery:
    def __init__(self, store):
        self.store, self._order, self._limit = store, None, None

    def order_by(self, field, direction="ASCENDING"):
        self._order = (field, str(direction).upper() == "DESCENDING")
        return self

    def limit(self, n):
        self._limit = n
        return self

    def stream(self):
        docs = [FakeDoc(self.store, i) for i in self.store]
        if self._order:
            field, desc = self._order
            docs.sort(key=lambda d: d.to_dict()[field], reverse=desc)
        return docs[: self._limit]


class FakeCollection:
    def __init__(self):
        self.store = {}

    def document(self, doc_id=None):
        return FakeDoc(self.store, doc_id or uuid.uuid4().hex[:20])

    def order_by(self, *args, **kwargs):
        return FakeQuery(self.store).order_by(*args, **kwargs)

    def limit(self, n):
        return FakeQuery(self.store).limit(n)

    def stream(self):
        return FakeQuery(self.store).stream()


class FakeFirestore:
    def __init__(self):
        self.collections = {}

    def collection(self, name):
        return self.collections.setdefault(name, FakeCollection())


@pytest.fixture
def client():
    fake_db = FakeFirestore()
    app.dependency_overrides[get_db] = lambda: fake_db
    yield TestClient(app)
    app.dependency_overrides.clear()
