"""
app.py — Minimal FastAPI server for Lesson 44.
In-memory user store; resets on restart.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import itertools

app = FastAPI(title="UQAP User Service Stub")

_id_counter = itertools.count(start=1)
_users: dict[int, dict] = {}


class UserIn(BaseModel):
    name: str
    email: str


class UserOut(BaseModel):
    id: int
    name: str
    email: str


@app.post("/users", response_model=UserOut, status_code=201)
def create_user(body: UserIn) -> UserOut:
    uid = next(_id_counter)
    _users[uid] = {"id": uid, "name": body.name, "email": body.email}
    return UserOut(**_users[uid])


@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int) -> UserOut:
    if user_id not in _users:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return UserOut(**_users[user_id])


@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int) -> None:
    _users.pop(user_id, None)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "user_count": len(_users)}
