import json
import numpy as np
import pandas as pd
import os
from app.engine.all_countries_loop import *
from app.engine.calc_benefit_types import *
from app.engine.sensitivity_analysis import *
from app.engine.calculations import read_database

np.seterr(divide="ignore", invalid="ignore")

dirname = os.path.dirname(__file__)
input_path = dirname + "/UNFPA_inputs_gradedGDPgrowth_20220802.xlsx"
output_path = dirname + "/UNFPA_BCR.xlsx"
json_output_path = dirname + "/UNFPA_BCR.json"

end_year = 2050
include_fp_stillbirth_mort = False

# Include all regions in BCR input sheet
regions = pd.read_excel(input_path, sheet_name="Mat lives saved")
regions = regions.values
region_list = regions[:, [0]].flatten()
region_list = ["Kenya"]

input_data = read_database(input_path)

# Include option to take out SB related to FP
main_results, daly_df = run_bcr_script(
    region_list=region_list,
    input_data=input_data,
    final_year=end_year,
    include_fp_stillbirth_mort=include_fp_stillbirth_mort,
    include_all_countries=len(region_list) > 1,
)

sens = run_sensitivity_analysis(
    region_list=region_list,
    input_data=input_data,
    outpath=output_path,
    final_year=end_year,
    main_results=main_results,
    daly_df=daly_df,
    include_fp_stillbirth_mort=include_fp_stillbirth_mort,
    include_all_countries=len(region_list) > 1,
    output_to_excel=False,
)

with open(json_output_path, "w") as f:
    json.dump(sens, f)
