# profiles.py
from fastapi import APIRouter, Depends, HTTPException
import json, os
from auth import get_current_user

router = APIRouter()
PROFILE_DIR = "profiles"


@router.post("/save")
def save_profile(profile: dict, user: str = Depends(get_current_user)):
    """Save a user's profile to a JSON file."""
    os.makedirs(PROFILE_DIR, exist_ok=True)
    filepath = f"{PROFILE_DIR}/{user}.json"

    with open(filepath, "w") as f:
        json.dump(profile, f, indent=4)

    return {"message": "Profile saved", "user": user}


@router.get("/me")
def load_profile(user: str = Depends(get_current_user)):
    """Load the user's saved profile."""
    filepath = f"{PROFILE_DIR}/{user}.json"

    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="No profile found")

    with open(filepath, "r") as f:
        profile = json.load(f)

    return profile
