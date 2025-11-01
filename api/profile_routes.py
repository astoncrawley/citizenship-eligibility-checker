# api/profile_routes.py
import os
import json
from fastapi import APIRouter, Depends, HTTPException
from .auth import _load_users, _save_users, get_current_user

router = APIRouter()


@router.post("/profile")
def save_profile(payload: dict, user: str = Depends(get_current_user)):
    """
    Save full PersonSchema JSON under the logged-in user.
    payload: the PersonSchema JSON (arbitrary dict)
    """
    top = _load_users()
    users = top.setdefault("users", {})
    if user not in users:
        raise HTTPException(status_code=404, detail="User not found")
    users[user]["profile"] = payload
    _save_users(top)
    return {"message": "profile saved", "user": user}


@router.get("/profile")
def get_profile(user: str = Depends(get_current_user)):
    top = _load_users()
    users = top.get("users", {})
    if user not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return {"profile": users[user].get("profile")}
