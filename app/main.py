from typing import Dict, List
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_camelcase import CamelModel
from app.engine.calculations import generate_report

VERSION = "0.1.2"


class Parameters(CamelModel):
    initial_year: int
    costs: List[float]
    unintended_pregnancies_averted: List[float]
    maternal_lives_saved_from_scaling_up_fp: List[float]
    maternal_lives_saved_from_mh_interventions: List[float]
    maternal_morbidities_averted: List[float]
    neonatal_lives_saved: List[float]
    stillbirths_averted: List[float]

    class Config:
        schema_extra = {
            "example": {
                "initial_year": 2022,
                "costs": [
                    67_215_311.68,
                    90_995_943.56,
                    115_438_886.8,
                    140_414_456.6,
                    165_718_637.1,
                    191_145_937.3,
                    215_844_534.3,
                    240_638_424.8,
                    264_004_169.4,
                ],
                "unintended_pregnancies_averted": [
                    68_401,
                    142_589,
                    222_697,
                    308_745,
                    400_823,
                    498_975,
                    603_317,
                    714_117,
                    831_654,
                ],
                "maternal_lives_saved_from_scaling_up_fp": [
                    208,
                    433,
                    676,
                    937,
                    1_217,
                    1_515,
                    1_832,
                    2_168,
                    2_525,
                ],
                "maternal_lives_saved_from_mh_interventions": [
                    626,
                    1_282,
                    1_819,
                    2_256,
                    2_596,
                    2_850,
                    3_018,
                    3_131,
                    3_167,
                ],
                "maternal_morbidities_averted": [
                    1357,
                    2829,
                    4418,
                    6125,
                    7952,
                    9899,
                    11969,
                    14167,
                    16498,
                ],
                "neonatal_lives_saved": [
                    1_568,
                    2_875,
                    4_050,
                    5_099,
                    6_021,
                    6_815,
                    7_448,
                    7_986,
                    8_350,
                ],
                "stillbirths_averted": [
                    2_708,
                    5_158,
                    7_375,
                    9_365,
                    11_125,
                    12_653,
                    13_886,
                    14_935,
                    15_669,
                ],
            }
        }


class Report(CamelModel):
    ...


app = FastAPI(
    title="BCR Calculator",
    description="API for generating country-level BCR reports",
    version=VERSION,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter(prefix="/api/v1", tags=["report"])


@router.get("/parameters/{country}", response_model=Parameters)
def get_parameters(country: str) -> Parameters:
    return Parameters(
        initial_year=2022,
        costs=[],
        unintended_pregnancies_averted=[],
        maternal_lives_saved_from_scaling_up_fp=[],
        maternal_lives_saved_from_mh_interventions=[],
        maternal_morbidities_averted=[],
        neonatal_lives_saved=[],
        stillbirths_averted=[],
    )


@router.post("/report/{country}", response_model=Dict)
def create_report(country, parameters: Parameters) -> Dict:
    return generate_report([country])


app.include_router(router)
