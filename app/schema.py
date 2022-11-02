from typing import List, Optional
from fastapi_camelcase import CamelModel


class DefaultParameters(CamelModel):
    country_code_numeric: Optional[int]
    country_code_alpha: Optional[str]
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
                "countryCodeAlpha": "KEN",
                "initialYear": 2022,
                "finalYear": 2030,
                "population": 53771300,
                "gdpPerCapita": 1838.21,
                "weightedGdpPerCapita": 2924.978114170695,
                "annualGdpGrowthRate": 0.025,
                "annualDiscountRate": 0.03,
                "proportionOfWomenInWorkforce": 0.7241,
                "averageAgeOfPregnancy": 28.697,
                "maternalMortalityRate": 280.580532767762,
                "neonatalMortalityRate": 21,
                "stillbirthRate": 19.7,
                "averageAnnualSalary": 4163.75,
                "workforceParticipationRate": 0.7456,
                "lifeExpectancy": 66.7,
                "mhCosts": [
                    22_048_052,
                    22_122_209,
                    22_078_877,
                    21_986_711,
                    21_845_835,
                    21_652_126,
                    21_309_124,
                    20_986_550,
                    20_498_428,
                ],
            }
        }


class CustomParameters(DefaultParameters):
    maternal_lives_saved_from_mh_interventions: List[float]
    neonatal_lives_saved: List[float]
    stillbirths_averted: List[float]
    unintended_pregnancies_averted: List[float]
    maternal_lives_saved_from_scaling_up_fp: List[float]

    class Config:
        schema_extra = {
            "example": {
                "initialYear": 2022,
                "finalYear": 2030,
                "population": 53771300,
                "gdpPerCapita": 1838.21,
                "weightedGdpPerCapita": 2924.978114170695,
                "annualGdpGrowthRate": 0.025,
                "annualDiscountRate": 0.03,
                "proportionOfWomenInWorkforce": 0.7241,
                "averageAgeOfPregnancy": 28.697,
                "maternalMortalityRate": 280.580532767762,
                "neonatalMortalityRate": 21,
                "stillbirthRate": 19.7,
                "averageAnnualSalary": 4163.75,
                "workforceParticipationRate": 0.7456,
                "lifeExpectancy": 66.7,
                "mhCosts": [
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
                "maternalLivesSavedFromMhInterventions": [
                    626.2826995823962,
                    1_282.0871304808752,
                    1_819.0815822284321,
                    2_255.8260886164007,
                    2_596.0511991368585,
                    2_850.2759499565595,
                    3_017.7254270522335,
                    3_131.0402686141774,
                    3_166.990796238436,
                ],
                "neonatalLivesSaved": [
                    1_567.916251073726,
                    2_874.9874222511353,
                    4_050.2717447362265,
                    5_099.166373696906,
                    6_020.710690504333,
                    6_814.664998495256,
                    7_447.946694597576,
                    7_986.129374411499,
                    8_349.707235760718,
                ],
                "stillbirthsAverted": [
                    2_708.1617036417883,
                    5_158.053272587902,
                    7_374.871256126309,
                    9_364.840309135056,
                    11_125.253407032484,
                    12_653.094193975747,
                    13_886.019861350132,
                    14_934.926290832747,
                    15_668.982363582001,
                ],
                "unintendedPregnanciesAverted": [
                    68_401.36730371183,
                    142_589.35347971413,
                    222_697.0775421029,
                    308_744.6357523389,
                    400_822.61365275783,
                    498_975.3685827963,
                    603_317.2522045672,
                    714_116.6537863165,
                    831_654.0701013869,
                ],
                "maternalLivesSavedFromScalingUpFp": [
                    207.67526922645084,
                    432.9194508823539,
                    676.1367112611824,
                    937.3880651741019,
                    1_216.948541873211,
                    1_514.9528158946086,
                    1_831.74807345915,
                    2_168.149178592772,
                    2_525.0077552500425,
                ],
            }
        }


class Report(CamelModel):
    ...
