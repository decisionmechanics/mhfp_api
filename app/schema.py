from typing import List
from fastapi_camelcase import CamelModel


class DefaultParameters(CamelModel):
    initial_year: int
    final_year: int
    population: int
    gdp_per_capita: float
    weighted_gdp_per_capita: float
    annual_gdp_growth_rate: float
    annual_discount_rate: float
    proportion_of_women_in_workforce: float
    average_age_of_pregnancy: float
    maternal_mortality_rate: float
    neonatal_mortality_rate: float
    stillbirth_rate: float
    average_annual_salary: float
    workforce_participation_rate: float
    life_expectancy: float
    mh_costs: List[float]

    class Config:
        schema_extra = {
            "example": {
                "initial_year": 2022,
                "final_year": 2030,
                "population": 53771300,
                "gdp_per_capita": 1838.21,
                "weighted_gdp_per_capita": 2924.98,
                "annual_gdp_growth_rate": 0.025,
                "annual_discount_rate": 0.03,
                "proportion_of_women_in_workforce": 0.724,
                "average_age_of_pregnancy": 28.7,
                "maternal_mortality_rate": 280.58,
                "neonatal_mortality_rate": 21,
                "stillbirth_rate": 19.7,
                "average_annual_salary": 4163.75,
                "workforce_participation_rate": 0.746,
                "life_expectancy": 66.7,
                "mh_costs": [
                    65_796_130,
                    87_952_418,
                    110_552_574,
                    133_455_860,
                    156_445_530,
                    179_304_244,
                    201_166_517,
                    222_838_578,
                    242_778_263,
                ],
            }
        }


class CustomParameters(DefaultParameters):
    maternal_lives_saved_from_mh_interventions: List[int]
    neonatal_lives_saved: List[int]
    stillbirths_averted: List[int]
    unintended_pregnancies_averted: List[int]
    maternal_lives_saved_from_scaling_up_fp: List[int]

    class Config:
        schema_extra = {
            "example": {
                "initial_year": 2022,
                "final_year": 2030,
                "population": 53771300,
                "gdp_per_capita": 1838.21,
                "weighted_gdp_per_capita": 2924.98,
                "annual_gdp_growth_rate": 0.025,
                "annual_discount_rate": 0.03,
                "proportion_of_women_in_workforce": 0.724,
                "average_age_of_pregnancy": 28.7,
                "maternal_mortality_rate": 280.58,
                "neonatal_mortality_rate": 21,
                "stillbirth_rate": 19.7,
                "average_annual_salary": 4163.75,
                "workforce_participation_rate": 0.746,
                "life_expectancy": 66.7,
                "mh_costs": [
                    65_796_130,
                    87_952_418,
                    110_552_574,
                    133_455_860,
                    156_445_530,
                    179_304_244,
                    201_166_517,
                    222_838_578,
                    242_778_263,
                ],
                "maternal_lives_saved_from_mh_interventions": [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                ],
                "neonatal_lives_saved": [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                ],
                "stillbirths_averted": [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                ],
                "unintended_pregnancies_averted": [
                    2_110_871,
                    2_188_650,
                    2_267_157,
                    2_346_052,
                    2_424_997,
                    2_503_557,
                    2_581_536,
                    2_658_603,
                    2_734_563,
                ],
                "maternalLivesSavedFromScalingUpFp": [
                    5_339,
                    5_466,
                    5_593,
                    5_719,
                    5_845,
                    5_968,
                    6_089,
                    6_206,
                    6_318,
                ],
            }
        }


class Report(CamelModel):
    ...
