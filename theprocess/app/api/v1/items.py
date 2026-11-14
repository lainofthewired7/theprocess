"""/api/v1/items - test resource showing the router -> service -> Firestore pattern."""
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from google.cloud.firestore import Client

from app.api.deps import get_db
from app.schemas.item import Item, ItemCreate, ItemUpdate
from app.services import item as item_service

router = APIRouter(prefix="/items", tags=["items"])


def _not_found(item_id: str) -> HTTPException:
    return HTTPException(status_code=404, detail=f"Item {item_id} not found")


@router.post("", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate, db: Client = Depends(get_db)):
    return item_service.create_item(db, item)


@router.get("", response_model=list[Item])
def list_items(limit: int = Query(default=10, ge=1, le=100), db: Client = Depends(get_db)):
    return item_service.list_items(db, limit)


@router.get("/{item_id}", response_model=Item)
def get_item(item_id: str, db: Client = Depends(get_db)):
    item = item_service.get_item(db, item_id)
    if item is None:
        raise _not_found(item_id)
    return item


@router.patch("/{item_id}", response_model=Item)
def update_item(item_id: str, changes: ItemUpdate, db: Client = Depends(get_db)):
    item = item_service.update_item(db, item_id, changes)
    if item is None:
        raise _not_found(item_id)
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: str, db: Client = Depends(get_db)):
    if not item_service.delete_item(db, item_id):
        raise _not_found(item_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
