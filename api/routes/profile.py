from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.profile import Profile
from models.person import Person
from database import get_db
from fastapi_users import current_user

router = APIRouter()

@router.post("/profile/save")
def save_profile(person: dict, user=Depends(current_user), db: Session = Depends(get_db)):
    profile = Profile(owner_id=user.id, person_data=person)
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return {"status": "saved", "profile_id": profile.id}

@router.get("/profile/me")
def get_profiles(user=Depends(current_user), db: Session = Depends(get_db)):
    profiles = db.query(Profile).filter(Profile.owner_id == user.id).all()
    return [p.person_data for p in profiles]
