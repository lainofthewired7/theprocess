"""Entry point. Run from the theprocess/ folder:  uvicorn app.main:app --reload"""
from fastapi import FastAPI

from app.api.v1 import items

app = FastAPI(title="The Process API")

API_PREFIX = "/api/v1"

# Add each router here as it gets built, e.g.:
# from app.api.v1 import users, entries, goals
# app.include_router(users.router, prefix=API_PREFIX)
app.include_router(items.router, prefix=API_PREFIX)


@app.get("/")
def health_check():
    return {"status": "ok"}
