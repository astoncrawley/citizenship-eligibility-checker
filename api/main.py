# from fastapi import FastAPI
# from api.routes import evaluate

# app = FastAPI(
#     title="Citizenship Eligibility API",
#     version="1.0.0",
#     description="API for checking eligibility for various citizenships."
# )

# app.include_router(evaluate.router, prefix="/citizenship", tags=["Citizenship"])

# @app.get("/")
# def root():
#     return {"message": "Welcome to the Citizenship Eligibility API"}


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from api.routes import evaluate

app = FastAPI(title="Citizenship Eligibility API")

# ✅ Add this CORS middleware block
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict to ["http://localhost:8000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(evaluate.router, prefix="/citizenship", tags=["Citizenship"])

# Serve static HTML form
app.mount("/", StaticFiles(directory="static", html=True), name="static")
