# import os
# import json
# from fastapi import APIRouter, Depends, Header, HTTPException
# from typing import Optional, Dict, Any
# from .auth import _load_users, _save_users, get_current_user

# router = APIRouter()

# PROFILE_DIR = "user_profiles"
# os.makedirs(PROFILE_DIR, exist_ok=True)

# def profile_path(email: str) -> str:
#     safe = email.replace("@", "_at_")
#     return os.path.join(PROFILE_DIR, f"{safe}.json")

# @router.post("/profile")
# def save_full_profile(data: Dict[str, Any], user=Depends(get_current_user)):
#     """Overwrites full profile."""
#     with open(profile_path(user["email"]), "w") as f:
#         json.dump(data, f, indent=2)
#     return {"status": "saved", "full": True}

# # @router.post("/profile")
# # def save_profile(payload: dict, user: str = Depends(get_current_user)):
# #     """
# #     Save full PersonSchema JSON under the logged-in user.
# #     payload: the PersonSchema JSON (arbitrary dict)
# #     """
# #     top = _load_users()
# #     users = top.setdefault("users", {})
# #     if user not in users:
# #         raise HTTPException(status_code=404, detail="User not found")
# #     users[user]["profile"] = payload
# #     _save_users(top)
# #     return {"message": "profile saved", "user": user}

# @router.get("/profile")
# def get_profile(user=Depends(get_current_user)):
#     path = profile_path(user["email"])
#     if not os.path.exists(path):
#         return {}  # Empty profile if none saved yet
#     with open(path, "r") as f:
#         return json.load(f)

# # @router.get("/profile")
# # def get_profile(user: str = Depends(get_current_user)):
# #     top = _load_users()
# #     users = top.get("users", {})
# #     if user not in users:
# #         raise HTTPException(status_code=404, detail="User not found")
# #     return {"profile": users[user].get("profile")}

# @router.patch("/profile")
# def update_profile(data: Dict[str, Any], user=Depends(get_current_user)):
#     """Merge update: only updates given fields."""
#     path = profile_path(user["email"])
#     current = {}

#     if os.path.exists(path):
#         with open(path, "r") as f:
#             current = json.load(f)

#     # Merge
#     merged = {**current, **data}

#     with open(path, "w") as f:
#         json.dump(merged, f, indent=2)

#     return {"status": "updated", "full": False}





# from fastapi import APIRouter, Depends, HTTPException, status
# from pydantic import BaseModel, Field
# from typing import List, Optional, Any, Dict
# from sqlalchemy.orm import Session
# from database import get_db
# from auth import get_current_user
# from models import User, UserProfile

# router = APIRouter(prefix="/api/profile", tags=["Profile"])


# # ----------- Pydantic Models (Format B) ------------ #

# class Citizenship(BaseModel):
#     country: str
#     method: str
#     date_acquired: Optional[str] = None  # can be blank


# class Parent(BaseModel):
#     name: Optional[str] = None
#     date_of_birth: Optional[str] = None
#     country_of_birth: Optional[str] = None
#     gender: Optional[str] = None
#     citizenships: List[Citizenship] = Field(default_factory=list)
#     marriages: List[Any] = Field(default_factory=list)  # reserved for future


# class Profile(BaseModel):
#     name: Optional[str] = None
#     date_of_birth: Optional[str] = None
#     country_of_birth: Optional[str] = None
#     gender: Optional[str] = None
#     parents: List[Parent] = Field(default_factory=list)
#     citizenships: List[Citizenship] = Field(default_factory=list)
#     marriages: List[Any] = Field(default_factory=list)  # reserved for future


# # ----------- Routes ------------ #

# @router.post("", response_model=dict)
# def save_profile(
#     profile: Profile,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     """Save or update the user's profile (Format B)."""
#     db_profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()

#     if db_profile:
#         db_profile.data = profile.dict()
#     else:
#         db_profile = UserProfile(user_id=current_user.id, data=profile.dict())
#         db.add(db_profile)

#     db.commit()
#     return {"message": "Profile saved successfully"}


# @router.get("", response_model=Profile)
# def load_profile(
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     """Load the user's profile in Format B."""
#     db_profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()

#     if not db_profile:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="No profile found for this user"
#         )

#     # Return stored data as a Profile object
#     return Profile(**db_profile.data)




import os
import json
from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from .auth import get_current_user

router = APIRouter()

PROFILE_DIR = "user_profiles"
os.makedirs(PROFILE_DIR, exist_ok=True)

def profile_path(email: str) -> str:
    safe = email.replace("@", "_at_")
    return os.path.join(PROFILE_DIR, f"{safe}.json")

@router.get("/profile")
def get_profile(user=Depends(get_current_user)):
    path = profile_path(user["email"])
    if not os.path.exists(path):
        return {}  # No profile yet
    with open(path, "r") as f:
        return json.load(f)

@router.post("/profile")
def save_full_profile(data: Dict[str, Any], user=Depends(get_current_user)):
    """Overwrite full profile with submitted JSON"""
    path = profile_path(user["email"])
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    return {"status": "saved", "full": True}

@router.patch("/profile")
def update_profile(data: Dict[str, Any], user=Depends(get_current_user)):
    """Merge update profile fields"""
    path = profile_path(user["email"])
    current = {}
    if os.path.exists(path):
        with open(path, "r") as f:
            current = json.load(f)

    current.update(data)

    with open(path, "w") as f:
        json.dump(current, f, indent=2)
    return {"status": "updated", "full": False}
