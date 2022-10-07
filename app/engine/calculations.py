import numpy as np
import os
from pathlib import Path
from app.engine.all_countries_loop import run_bcr_script
from app.engine.sensitivity_analysis import run_sensitivity_analysis
from app.engine.utilities import collate_results

np.seterr(divide="ignore", invalid="ignore")

database_path = (
    Path(__file__).parent.absolute() / "UNFPA_inputs_gradedGDPgrowth_20220802.xlsx"
)


def generate_report(countries):
    FINAL_YEAR = 2050
    INCLUDE_FP_STILLBIRTH_MORTALITY = False

    main_df, daly_df = run_bcr_script(
        region_list=countries,
        inpath=database_path,
        outpath=None,
        final_year=FINAL_YEAR,
        include_fp_stillbirth_mort=INCLUDE_FP_STILLBIRTH_MORTALITY,
        include_all_countries=False,
    )

    return run_sensitivity_analysis(
        region_list=countries,
        inpath=database_path,
        outpath=None,
        final_year=FINAL_YEAR,
        main_results=main_df,
        daly_df=daly_df,
        include_fp_stillbirth_mort=INCLUDE_FP_STILLBIRTH_MORTALITY,
        include_all_countries=False,
        output_to_excel=False,
    )


if __name__ == "__main__":
    print(generate_report(["Kenya"]))
