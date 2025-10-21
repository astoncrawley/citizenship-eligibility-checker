from fastapi import FastAPI
from api.routes import evaluate

app = FastAPI(
    title="Citizenship Eligibility API",
    version="1.0.0",
    description="API for checking eligibility for various citizenships."
)

app.include_router(evaluate.router, prefix="/citizenship", tags=["Citizenship"])

@app.get("/")
def root():
    return {"message": "Welcome to the Citizenship Eligibility API"}
