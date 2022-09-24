import numpy as np
import pandas as pd
import os
from all_countries_loop import *
from sensitivity_analysis import *
from calc_benefit_types import *

np.seterr(divide="ignore", invalid="ignore")

dirname = os.path.dirname(__file__)
input_path = dirname + "/UNFPA_inputs_gradedGDPgrowth_20220802.xlsx"
output_path = dirname + "/UNFPA_BCR.xlsx"

end_year = 2050
include_fp_stillbirth_mort = False

# Include all regions in BCR input sheet
regions = pd.read_excel(input_path, sheet_name="Mat lives saved")
regions = regions.values
region_list = regions[:, [0]].flatten()

# Include option to take out SB related to FP
main_results, daly_df = run_bcr_script(
    region_list=region_list,
    inpath=input_path,
    outpath=output_path,
    final_year=end_year,
    include_fp_stillbirth_mort=include_fp_stillbirth_mort,
)
sens = run_sensitivity_analysis(
    region_list=region_list,
    inpath=input_path,
    outpath=output_path,
    final_year=end_year,
    main_results=main_results,
    daly_df=daly_df,
    include_fp_stillbirth_mort=include_fp_stillbirth_mort,
)
