import os
import json
from fastapi import APIRouter, Depends, Header, HTTPException
from typing import Optional, Dict, Any
from .auth import _load_users, _save_users, get_current_user

router = APIRouter()

PROFILE_DIR = "user_profiles"
os.makedirs(PROFILE_DIR, exist_ok=True)

def profile_path(email: str) -> str:
    safe = email.replace("@", "_at_")
    return os.path.join(PROFILE_DIR, f"{safe}.json")

@router.post("/profile")
def save_full_profile(data: Dict[str, Any], user=Depends(get_current_user)):
    """Overwrites full profile."""
    with open(profile_path(user["email"]), "w") as f:
        json.dump(data, f, indent=2)
    return {"status": "saved", "full": True}

# @router.post("/profile")
# def save_profile(payload: dict, user: str = Depends(get_current_user)):
#     """
#     Save full PersonSchema JSON under the logged-in user.
#     payload: the PersonSchema JSON (arbitrary dict)
#     """
#     top = _load_users()
#     users = top.setdefault("users", {})
#     if user not in users:
#         raise HTTPException(status_code=404, detail="User not found")
#     users[user]["profile"] = payload
#     _save_users(top)
#     return {"message": "profile saved", "user": user}

@router.get("/profile")
def get_profile(user=Depends(get_current_user)):
    path = profile_path(user["email"])
    if not os.path.exists(path):
        return {}  # Empty profile if none saved yet
    with open(path, "r") as f:
        return json.load(f)

# @router.get("/profile")
# def get_profile(user: str = Depends(get_current_user)):
#     top = _load_users()
#     users = top.get("users", {})
#     if user not in users:
#         raise HTTPException(status_code=404, detail="User not found")
#     return {"profile": users[user].get("profile")}

@router.patch("/profile")
def update_profile(data: Dict[str, Any], user=Depends(get_current_user)):
    """Merge update: only updates given fields."""
    path = profile_path(user["email"])
    current = {}

    if os.path.exists(path):
        with open(path, "r") as f:
            current = json.load(f)

    # Merge
    merged = {**current, **data}

    with open(path, "w") as f:
        json.dump(merged, f, indent=2)

    return {"status": "updated", "full": False}
