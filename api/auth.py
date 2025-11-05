# import os
# import json
# import hashlib
# from datetime import datetime, timedelta

# from fastapi import APIRouter, HTTPException, Depends, Header
# from fastapi.security import OAuth2PasswordRequestForm
# import jwt  # pip install pyjwt

# router = APIRouter()
# DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
# os.makedirs(DATA_DIR, exist_ok=True)
# USERS_FILE = os.path.join(DATA_DIR, "users.json")

# SECRET_KEY = os.environ.get("JWT_SECRET", "please_change_this_secret")
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day

# # ensure file exists
# if not os.path.exists(USERS_FILE):
#     with open(USERS_FILE, "w", encoding="utf-8") as f:
#         json.dump({"users": {}}, f, indent=2)


# def _load_users():
#     with open(USERS_FILE, "r", encoding="utf-8") as f:
#         return json.load(f)


# def _save_users(data):
#     with open(USERS_FILE, "w", encoding="utf-8") as f:
#         json.dump(data, f, indent=2)


# def _hash_password(password: str) -> str:
#     return hashlib.sha256(password.encode()).hexdigest()


# def create_access_token(subject: str, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES):
#     expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
#     payload = {"sub": subject, "exp": expire.isoformat()}
#     token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
#     return token


# def get_current_user(authorization: str = Header(None)):
#     """
#     Expects header: Authorization: Bearer <token>
#     Returns: user email (subject) or raises 401
#     """
#     if not authorization:
#         raise HTTPException(status_code=401, detail="Missing Authorization header")
#     try:
#         scheme, token = authorization.split(" ")
#         if scheme.lower() != "bearer":
#             raise HTTPException(status_code=401, detail="Invalid auth scheme")
#     except ValueError:
#         raise HTTPException(status_code=401, detail="Invalid Authorization header format")

#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         subject = payload.get("sub")
#         if not subject:
#             raise HTTPException(status_code=401, detail="Invalid token payload")
#         users = _load_users().get("users", {})
#         if subject not in users:
#             raise HTTPException(status_code=401, detail="User not found")
#         return subject
#     except jwt.ExpiredSignatureError:
#         raise HTTPException(status_code=401, detail="Token expired")
#     except Exception:
#         raise HTTPException(status_code=401, detail="Invalid token")


# @router.post("/register")
# def register(payload: dict):
#     email = payload.get("email")
#     password = payload.get("password")
#     if not email or not password:
#         raise HTTPException(status_code=400, detail="email and password required")
#     top = _load_users()
#     users = top.setdefault("users", {})
#     if email in users:
#         raise HTTPException(status_code=409, detail="User already exists")
#     users[email] = {
#         "password_hash": _hash_password(password),
#         "profile": None
#     }
#     _save_users(top)
#     return {"message": "registered", "email": email}


# @router.post("/login")
# def login(payload: dict):
#     email = payload.get("email")
#     password = payload.get("password")
#     if not email or not password:
#         raise HTTPException(status_code=400, detail="email and password required")
#     top = _load_users()
#     users = top.get("users", {})
#     user = users.get(email)
#     if not user or user.get("password_hash") != _hash_password(password):
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#     token = create_access_token(email)
#     return {"access_token": token, "token_type": "bearer"}





# import os
# import json
# import hashlib
# import uuid
# from fastapi import APIRouter, HTTPException, Header, Depends

# router = APIRouter()

# USERS_FILE = "users.json"

# def _load_users():
#     if not os.path.exists(USERS_FILE):
#         return {"users": {}}
#     with open(USERS_FILE, "r") as f:
#         return json.load(f)

# def _save_users(data):
#     with open(USERS_FILE, "w") as f:
#         json.dump(data, f, indent=2)

# def hash_pw(pw: str) -> str:
#     return hashlib.sha256(pw.encode()).hexdigest()

# @router.post("/register")
# def register_user(email: str, password: str):
#     if not email or not password:
#         raise HTTPException(status_code=400, detail="email and password required")

#     top = _load_users()
#     users = top["users"]

#     if email in users:
#         raise HTTPException(status_code=400, detail="email already registered")

#     token = str(uuid.uuid4())
#     users[email] = {"password": hash_pw(password), "token": token}
#     _save_users(top)

#     return {"message": "registered", "email": email}

# @router.post("/login")
# def login_user(email: str, password: str):
#     top = _load_users()
#     users = top["users"]

#     if email not in users or users[email]["password"] != hash_pw(password):
#         raise HTTPException(status_code=401, detail="invalid credentials")

#     token = users[email]["token"]
#     return {"access_token": token, "token_type": "bearer"}

# def get_current_user(authorization: str = Header(None)):
#     """
#     Expects: Authorization: Bearer <token>
#     """
#     if not authorization:
#         raise HTTPException(status_code=401, detail="Missing Authorization header")

#     if not authorization.lower().startswith("bearer "):
#         raise HTTPException(status_code=401, detail="Invalid auth format (expected: Bearer <token>)")

#     token = authorization.split(" ", 1)[1].strip()

#     top = _load_users()
#     users = top["users"]

#     for email, data in users.items():
#         if data.get("token") == token:
#             return {"email": email}

#     raise HTTPException(status_code=401, detail="Invalid token")



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
