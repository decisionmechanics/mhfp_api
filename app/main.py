from pathlib import Path
from typing import Dict
from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.engine.calculations import generate_report, get_country_df, read_database
from app.engine.countries import get_country_name
from app.schema import CustomParameters, DefaultParameters, Report

VERSION = "0.1.5"


app = FastAPI(
    title="Child Survival Family Planning (CSFP) API",
    description="API for generating country-level child survival family planning reports",
    version=VERSION,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter(prefix="/api/v1")


@router.get(
    "/parameters/{country_code}",
    response_model=DefaultParameters,
    tags=["parameters"],
    summary="Fetch default parameters for a country",
)
def get_parameters(
    country_code: str,
    request: Request,
    initial_year: int = 2022,
    final_year: int = 2030,
) -> DefaultParameters:
    country = get_country_name(country_code)

    database = request.app.state.database

    constants_df = get_country_df(database["BCR inputs constant"], country)
    mh_costs_df = get_country_df(database["MH costs"], country)

    initial_year = max(initial_year, 2021)
    final_year = min(final_year, 2030)

    return DefaultParameters(
        initial_year=initial_year,
        final_year=final_year,
        population=constants_df["Population"].values[0],
        gdp_per_capita=constants_df["GDP per capita"].values[0],
        weighted_gdp_per_capita=constants_df["GDP per capita weighted"].values[0],
        annual_gdp_growth_rate=constants_df["Annual GDP growth"].values[0],
        annual_discount_rate=constants_df["Discounting"].values[0],
        proportion_of_women_in_workforce=constants_df[
            "Proportion of women who participate in workforce"
        ].values[0],
        average_age_of_pregnancy=constants_df["Average age of pregnancy"].values[0],
        maternal_mortality_rate=constants_df["Maternal mortality rate"].values[0],
        neonatal_mortality_rate=constants_df["Neonatal mortality rate"].values[0],
        stillbirth_rate=constants_df["Stillbirth rate"].values[0],
        average_annual_salary=constants_df["Average annual salary"].values[0],
        workforce_participation_rate=constants_df["Workforce participation"].values[0],
        life_expectancy=constants_df["Life expectancy"].values[0],
        mh_costs=(
            mh_costs_df[[f"{year}.1" for year in range(initial_year, final_year + 1)]]
            .values[0]
            .tolist()
        ),
    )


@router.post(
    "/report/default/{country_code}",
    response_model=Dict,
    tags=["report"],
    summary="Generate a country report using default parameters",
)
def create_report(country_code, request: Request) -> Dict:
    country = get_country_name(country_code)

    return generate_report(request.app.state.database, country)


@router.post(
    "/report/{country_code}",
    response_model=Dict,
    tags=["report"],
    summary="Generate a country report using custom parameters",
)
def create_report(country_code, parameters: CustomParameters, request: Request) -> Dict:
    country = get_country_name(country_code)

    return generate_report(request.app.state.database, country, parameters)


app.include_router(router)


@app.on_event("startup")
async def startup():
    input_path = (
        Path(__file__).parent / "engine" / "UNFPA_inputs_gradedGDPgrowth_20220802.xlsx"
    )

    app.state.database = read_database(str(input_path))
