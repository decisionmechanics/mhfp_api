from functools import cache
import json
import pandas as pd


@cache
def read_data(file_path, sheet_name):
    return pd.read_excel(file_path, sheet_name=sheet_name)


def collate_results(report_names, main_df, sensitivity_analysis_dfs, daly_df):
    data = {}

    main_json = main_df.to_json(orient="records")
    data[report_names[0]] = json.loads(main_json)

    data["sensitivity_analysis"] = {}

    for report_name, sensitivity_analysis_df in zip(
        report_names[1:-1], sensitivity_analysis_dfs
    ):
        sensitivity_analysis_json = sensitivity_analysis_df.to_json(orient="records")
        data["sensitivity_analysis"][report_name] = json.loads(
            sensitivity_analysis_json
        )

    daly_json = daly_df.to_json(orient="records")
    data[report_names[-1]] = json.loads(daly_json)

    return data
