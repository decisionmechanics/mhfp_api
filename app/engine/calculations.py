from pathlib import Path
import numpy as np
import pandas as pd
from app.engine.all_countries_loop import run_bcr_script
from app.engine.maternal_morbidities import calculate_maternal_morbidities_averted
from app.engine.sensitivity_analysis import run_sensitivity_analysis
from app.engine.utilities import parse_alpha_country_code, parse_numeric_country_code

DEFAULT_INITIAL_YEAR = 2022

np.seterr(divide="ignore", invalid="ignore")

database_path = (
    Path(__file__).parent.absolute() / "UNFPA_inputs_gradedGDPgrowth_20220802.xlsx"
)


def read_database(database_path):
    sheet_names = [
        "Mat lives saved",
        "Neo lives saved",
        "Stillbirths averted",
        "Unintended pregnancies averted",
        "Child lives saved",
        "FP_Mat lives saved",
        "Mat morbidities averted",
        "Neo morbidites averted",
        "Wasting averted",
        "Stunting averted",
        "BCR inputs constant",
        "FP costs discounted",
        "MH costs",
    ]

    xlsx = pd.ExcelFile(database_path)

    return {sheet_name: xlsx.parse(sheet_name=sheet_name) for sheet_name in sheet_names}


def get_country_df(df, country):
    return df[df["Country"] == country].copy()


def generate_custom_database(database, country, parameters):
    constants_df = get_country_df(database["BCR inputs constant"], country)

    constants_df["Population"] = parameters.population
    constants_df["GDP per capita"] = parameters.gdp_per_capita
    constants_df["GDP per capita weighted"] = parameters.weighted_gdp_per_capita
    constants_df["Annual GDP growth"] = parameters.annual_gdp_growth_rate
    constants_df["Discounting"] = parameters.annual_discount_rate
    constants_df[
        "Proportion of women who participate in workforce"
    ] = parameters.proportion_of_women_in_workforce
    constants_df["Average age of pregnancy"] = parameters.average_age_of_pregnancy
    constants_df["Maternal mortality rate"] = parameters.maternal_mortality_rate
    constants_df["Neonatal mortality rate"] = parameters.neonatal_mortality_rate
    constants_df["Stillbirth rate"] = parameters.stillbirth_rate
    constants_df["Average annual salary"] = parameters.average_annual_salary
    constants_df["Workforce participation"] = parameters.workforce_participation_rate
    constants_df["Life expectancy"] = parameters.life_expectancy

    discounted_fp_costs_df = get_country_df(database["FP costs discounted"], country)
    maternal_lives_saved_from_mh_interventions_df = get_country_df(
        database["Mat lives saved"], country
    )
    neonatal_lives_saved_df = get_country_df(database["Neo lives saved"], country)
    stillbirths_averted_df = get_country_df(database["Stillbirths averted"], country)
    unintended_pregnancies_averted_df = get_country_df(
        database["Unintended pregnancies averted"], country
    )
    maternal_lives_saved_from_scaling_up_fp_df = get_country_df(
        database["FP_Mat lives saved"], country
    )
    maternal_morbidities_averted_df = get_country_df(
        database["Mat morbidities averted"], country
    )

    total_discounted_fp_costs = 0
    total_discounted_mh_costs = 0

    for index, year in enumerate(
        range(parameters.initial_year, parameters.final_year + 1)
    ):
        total_discounted_fp_costs += discounted_fp_costs_df[year]

        discount_factor = 1 / (1 + parameters.annual_discount_rate) ** (year - 2020)
        total_discounted_mh_costs += parameters.mh_costs[index] * discount_factor

        maternal_lives_saved_from_mh_interventions_df[
            year
        ] = parameters.maternal_lives_saved_from_mh_interventions[index]
        neonatal_lives_saved_df[year] = parameters.neonatal_lives_saved[index]
        stillbirths_averted_df[year] = parameters.stillbirths_averted[index]
        unintended_pregnancies_averted_df[
            year
        ] = parameters.unintended_pregnancies_averted[index]

        maternal_lives_saved_from_scaling_up_fp = (
            parameters.maternal_lives_saved_from_scaling_up_fp[index]
        )

        maternal_lives_saved_from_scaling_up_fp_df[
            year
        ] = maternal_lives_saved_from_scaling_up_fp
        maternal_morbidities_averted_df[year] = calculate_maternal_morbidities_averted(
            country, maternal_lives_saved_from_scaling_up_fp
        )

    constants_df["Total expenditure"] = (
        total_discounted_fp_costs + total_discounted_mh_costs
    )

    custom_database = database.copy()

    custom_database["Mat lives saved"] = maternal_lives_saved_from_mh_interventions_df
    custom_database["Neo lives saved"] = neonatal_lives_saved_df
    custom_database["Stillbirths averted"] = stillbirths_averted_df
    custom_database[
        "Unintended pregnancies averted"
    ] = unintended_pregnancies_averted_df
    custom_database["FP_Mat lives saved"] = maternal_lives_saved_from_scaling_up_fp_df
    custom_database["Mat morbidities averted"] = maternal_morbidities_averted_df
    custom_database["BCR inputs constant"] = constants_df

    return custom_database


def format_report(report):
    for item in report["Main results"]:
        del item["Region"]

        if item["Package"] == "":
            del item["Package"]

    for item in report["sensitivity_analysis"].values():
        for subitem in item:
            del subitem["Region"]

            if subitem["Package"] == "":
                del subitem["Package"]


def format_maternal_morbidities_averted(
    country, parameters, maternal_morbidities_averted_df
):
    initial_year = (
        DEFAULT_INITIAL_YEAR if parameters is None else parameters.initial_year
    )

    return (
        maternal_morbidities_averted_df.loc[
            maternal_morbidities_averted_df["Country"] == country, initial_year:2030
        ]
        .iloc[0]
        .to_dict()
    )


def generate_report(database, country_code, country, parameters=None):
    FINAL_YEAR = 2050
    INCLUDE_FP_STILLBIRTH_MORTALITY = False

    custom_database = (
        generate_custom_database(database, country, parameters)
        if parameters
        else database
    )

    main_df, daly_df = run_bcr_script(
        region_list=[country],
        input_data=custom_database,
        final_year=FINAL_YEAR,
        include_fp_stillbirth_mort=INCLUDE_FP_STILLBIRTH_MORTALITY,
        include_all_countries=False,
    )

    report = run_sensitivity_analysis(
        region_list=[country],
        input_data=custom_database,
        outpath=None,
        final_year=FINAL_YEAR,
        main_results=main_df,
        daly_df=daly_df,
        include_fp_stillbirth_mort=INCLUDE_FP_STILLBIRTH_MORTALITY,
        include_all_countries=False,
        output_to_excel=False,
    )

    format_report(report)

    maternal_morbidities_averted = format_maternal_morbidities_averted(
        country, parameters, custom_database["Mat morbidities averted"]
    )

    report["Maternal morbidities averted"] = maternal_morbidities_averted
    report["ISO country code"] = country_code.rjust(3, "0")
    report["Projected year"] = FINAL_YEAR

    return report


def main():
    database = read_database(
        Path(__file__).parent / "UNFPA_inputs_gradedGDPgrowth_20220802.xlsx"
    )
    print(generate_report(database, "Kenya"))


if __name__ == "__main__":
    main()
