import numpy as np
import os
from pathlib import Path
from app.engine.all_countries_loop import run_bcr_script
from app.engine.sensitivity_analysis import run_sensitivity_analysis
from app.engine.utilities import collate_results, read_data

np.seterr(divide="ignore", invalid="ignore")

database_path = (
    Path(__file__).parent.absolute() / "UNFPA_inputs_gradedGDPgrowth_20220802.xlsx"
)


def read_all_data(database_path):
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
    ]

    return {
        sheet_name: read_data(database_path, sheet_name=sheet_name)
        for sheet_name in sheet_names
    }


def remove_empty_packages(report):
    for item in report["Main results"]:
        if item["Package"] == "":
            del item["Package"]

    for item in report["sensitivity_analysis"].values():
        for subitem in item:
            if subitem["Package"] == "":
                del subitem["Package"]


def generate_report(countries):
    FINAL_YEAR = 2050
    INCLUDE_FP_STILLBIRTH_MORTALITY = False

    input_data = read_all_data(database_path)

    main_df, daly_df = run_bcr_script(
        region_list=countries,
        input_data=input_data,
        final_year=FINAL_YEAR,
        include_fp_stillbirth_mort=INCLUDE_FP_STILLBIRTH_MORTALITY,
        include_all_countries=False,
    )

    report = run_sensitivity_analysis(
        region_list=countries,
        input_data=input_data,
        outpath=None,
        final_year=FINAL_YEAR,
        main_results=main_df,
        daly_df=daly_df,
        include_fp_stillbirth_mort=INCLUDE_FP_STILLBIRTH_MORTALITY,
        include_all_countries=False,
        output_to_excel=False,
    )

    remove_empty_packages(report)

    return report


if __name__ == "__main__":
    print(generate_report(["Kenya"]))
