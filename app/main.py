from typing import Dict
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.engine.calculations import generate_report

VERSION = "0.1.1"

app = FastAPI(
    title="BCR Calculator",
    description="API for doing BCR calculations at country level",
    version=VERSION,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/report/{country}", tags=["report"])
async def get_report(country) -> Dict:
    return generate_report([country])
