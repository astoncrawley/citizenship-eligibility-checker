# app.py
from fastapi import FastAPI
from auth import router as auth_router
from profiles import router as profile_router

app = FastAPI(title="Minimal Auth + Profile Save")

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(profile_router, prefix="/profile", tags=["Profiles"])


@app.get("/")
def root():
    return {"message": "Server running. Use /auth/register, /auth/login, /profile/save"}
