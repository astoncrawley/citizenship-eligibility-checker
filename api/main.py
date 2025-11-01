# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles
# from api.routes import evaluate

# app = FastAPI(title="Citizenship Eligibility API")
# # app = FastAPI(
# #     title="Citizenship Eligibility API",
# #     version="1.0.0",
# #     description="API for checking eligibility for various citizenships."
# # )

# # ✅ Add this CORS middleware block
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # or restrict to ["http://localhost:8000"]
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Include API routes
# app.include_router(evaluate.router, prefix="/citizenship", tags=["Citizenship"])

# # Serve static HTML form
# app.mount("/", StaticFiles(directory="static", html=True), name="static")

# # @app.get("/")
# # def root():
# #     return {"message": "Welcome to the Citizenship Eligibility API"}






# from fastapi import FastAPI
# from fastapi_users import FastAPIUsers
# from fastapi_users.db import SQLAlchemyUserDatabase
# from fastapi_users.authentication import JWTStrategy
# from models.user import User
# from database import get_user_db, engine, Base

# app = FastAPI()

# def get_jwt_strategy() -> JWTStrategy:
#     return JWTStrategy(secret="SECRET_KEY", lifetime_seconds=3600)

# fastapi_users = FastAPIUsers[User, int](
#     get_user_db,
#     [get_jwt_strategy()],
# )

# app.include_router(fastapi_users.get_auth_router(get_jwt_strategy()), prefix="/auth/jwt", tags=["auth"])
# app.include_router(fastapi_users.get_register_router(), prefix="/auth", tags=["auth"])






# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles
# from .auth import router as auth_router
# from .profile_routes import router as profile_router

# app = FastAPI(title="Citizenship API (auth+profile)")

# # Allow same origin + development hosts; tighten for production
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Serve static HTML form
# app.mount("/", StaticFiles(directory="static", html=True), name="static")

# app.include_router(auth_router, prefix="/auth", tags=["auth"])
# app.include_router(profile_router, prefix="/api", tags=["profile"])

# @app.get("/")
# def root():
#     return {"message": "API running. Use /auth/register, /auth/login, /api/profile"}






from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .auth import router as auth_router
from .profile_routes import router as profile_router

app = FastAPI(title="Citizenship API (auth+profile)")

# Allow same origin + dev hosts; tighten for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Serve static HTML at /static instead of /
# app.mount("/", StaticFiles(directory="static", html=True), name="static")
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

# ✅ These now work as documented
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(profile_router, prefix="/api", tags=["profile"])

@app.get("/")
def root():
    return {
        "message": "API running.",
        "auth_endpoints": ["/auth/register", "/auth/login"],
        "profile_endpoints": ["/api/profile"],
        "ui": "Visit /static/index.html to view the form"
    }

# from fastapi.responses import RedirectResponse

# @app.get("/", include_in_schema=False)
# def root():
#     return RedirectResponse("/static/index.html")