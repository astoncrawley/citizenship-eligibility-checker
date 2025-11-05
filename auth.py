# # auth.py
# from fastapi import APIRouter, HTTPException, Depends
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from datetime import datetime, timedelta
# import jwt
# import hashlib

# # In-memory user "database"
# USERS = {}  # {email: {"password_hash": "..."}}

# SECRET_KEY = "SUPER_SECRET_KEY"  # change for production
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 60

# router = APIRouter()
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# def hash_password(password: str) -> str:
#     return hashlib.sha256(password.encode()).hexdigest()


# def create_access_token(email: str):
#     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     return jwt.encode({"sub": email, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)


# def get_current_user(token: str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email = payload.get("sub")
#         if email not in USERS:
#             raise HTTPException(status_code=401, detail="User not found")
#         return email
#     except Exception:
#         raise HTTPException(status_code=401, detail="Invalid token")


# @router.post("/register")
# def register(email: str, password: str):
#     if email in USERS:
#         raise HTTPException(status_code=400, detail="User already exists")
#     USERS[email] = {"password_hash": hash_password(password)}
#     return {"message": "User registered", "email": email}


# @router.post("/login")
# def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     email = form_data.username
#     password = form_data.password

#     if email not in USERS or USERS[email]["password_hash"] != hash_password(password):
#         raise HTTPException(status_code=401, detail="Invalid credentials")

#     token = create_access_token(email)
#     return {"access_token": token, "token_type": "bearer"}




# # auth.py
# import json
# import os
# from typing import Optional

# USERS_FILE = "profiles/users.json"

# # Ensure folder exists
# os.makedirs("profiles", exist_ok=True)

# # Initialize file if missing
# if not os.path.exists(USERS_FILE):
#     with open(USERS_FILE, "w") as f:
#         json.dump({}, f)


# def load_users() -> dict:
#     with open(USERS_FILE, "r") as f:
#         return json.load(f)


# def save_users(users: dict) -> None:
#     with open(USERS_FILE, "w") as f:
#         json.dump(users, f, indent=2)


# def register_user(username: str, password: str) -> bool:
#     users = load_users()
#     if username in users:
#         return False  # already exists

#     users[username] = {"password": password, "profile": {}}
#     save_users(users)
#     return True


# def authenticate(username: str, password: str) -> bool:
#     users = load_users()
#     return username in users and users[username]["password"] == password


# def save_profile(username: str, profile: dict) -> None:
#     users = load_users()
#     users[username]["profile"] = profile
#     save_users(users)


# def load_profile(username: str) -> Optional[dict]:
#     users = load_users()
#     return users.get(username, {}).get("profile")



import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any

from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel
import jwt

SECRET_KEY = "dev-secret-key"  # change in production
ALGORITHM = "HS256"
USERS_FILE = "users.json"

router = APIRouter()

# --------- Pydantic Model for JSON body ---------
class AuthData(BaseModel):
    email: str
    password: str


# --------- User Store Helpers (JSON FILE) ---------
def _load_users() -> Dict[str, Any]:
    if not os.path.exists(USERS_FILE):
        return {"users": {}}
    with open(USERS_FILE, "r") as f:
        return json.load(f)


def _save_users(data: Dict[str, Any]):
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=2)


# --------- JWT Helpers ---------
def create_token(email: str) -> str:
    payload = {
        "sub": email,
        "exp": datetime.utcnow() + timedelta(hours=12)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    token = authorization.split(" ", 1)[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    users = _load_users().get("users", {})
    if email not in users:
        raise HTTPException(status_code=401, detail="User no longer exists")

    return users[email]


# --------- AUTH ENDPOINTS ---------
@router.post("/register")
def register_user(data: AuthData):
    email = data.email
    password = data.password

    store = _load_users()
    users = store.setdefault("users", {})

    if email in users:
        raise HTTPException(status_code=400, detail="Email already registered")

    users[email] = {"email": email, "password": password, "profile": {}}
    _save_users(store)

    return {"message": "registered", "email": email}


@router.post("/login")
def login_user(data: AuthData):
    email = data.email
    password = data.password

    store = _load_users()
    users = store.get("users", {})

    if email not in users or users[email]["password"] != password:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_token(email)
    return {"access_token": token, "token_type": "bearer"}
