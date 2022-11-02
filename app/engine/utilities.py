import json
import pandas as pd


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


def parse_numeric_country_code(country_code):
    return int(country_code) if str.isnumeric(country_code) else None


def parse_alpha_country_code(country_code):
    return country_code if not str.isnumeric(country_code) else None
