from app.engine.all_countries_loop import *
from app.engine.utilities import collate_results


def run_sensitivity_analysis(
    region_list,
    input_data,
    outpath,
    final_year,
    main_results,
    daly_df,
    include_fp_stillbirth_mort,
    include_all_countries=True,
    output_to_excel=True,
):
    """
    A set of loops through parameters for sensitivity analyses. It's trivial to add another parameter, just copy the
    loop structure and add an additional sheet to the output file at the end. Note that sensitivity analyses for additional
    parameters will need to be manually added to the summary plot files.
    :param: region_List: List of regions considered in the analysis (can be country name if it is a national analysis only.)
    :param input_data: dictionary containing data from BCR input file (most likely summary sheet)
    :param outpath: file path for BCR outputs
    """

    output_filepath = outpath
    total_cost = [0]
    for r, region in enumerate(region_list):
        print(f"Performing sensitivty analysis for {region}")
        for p, package in enumerate([""]):
            (
                pars_country,
                preg_avert,
                mat_death,
                mat_morb,
                neo_death,
                neo_morb,
                child_death,
                child_morb,
                stillbirth,
            ) = read_benefit_params(region + package, input_data)
            total_cost = total_cost + pars_country["Total expenditure"][0]
            discount_totals = []
            for discount in [0, pars_country["Discounting"][0], 0.06]:
                orig = pars_country["Discounting"][0]
                pars_country["Discounting"] = discount
                benefits = total_econ_benefits(
                    pars_country,
                    preg_avert,
                    mat_death,
                    mat_morb,
                    neo_death,
                    neo_morb,
                    child_death,
                    child_morb,
                    stillbirth,
                    start_year=2022,
                    end_year=final_year,
                    include_fp_stillbirth_mort=include_fp_stillbirth_mort,
                )
                discount_totals.append(benefits)
                pars_country["Discounting"] = orig
                label_data = {
                    "Benefit cause": [
                        "Total benefit",
                        "Maternal death averted benefit",
                        "Neonatal death averted benefit",
                        "Child death averted benefit",
                        "Stillbirth averted benefit",
                        "Teenage pregnancy averted education benefit",
                        "Pregnancy averted work benefit",
                        "Total work benefits",
                        "Total education benefits",
                        "Total social benefits",
                        "Total BCR",
                        "Labour % of benefits",
                        "Education % of benefits",
                        "Social % of benefits",
                    ]
                }
            label_data = {"Benefit cause": [ben for ben in label_data["Benefit cause"]]}
            total_data = {
                "Discount rate: "
                + str(round(discount, 2))
                + ", Benefits": discount_totals[d]
                for d, discount in enumerate([0, pars_country["Discounting"][0], 0.06])
            }
            combine_data = {**label_data, **total_data}
            if r == 0 and p == 0:
                compiled_discount_df = pd.DataFrame(data=combine_data)
                compiled_discount_df.insert(
                    0, "Region", [region] * len(combine_data["Benefit cause"])
                )
                compiled_discount_df.insert(
                    0, "Package", [package] * len(combine_data["Benefit cause"])
                )
            else:
                compiled_discount0 = pd.DataFrame(data=combine_data)
                compiled_discount0.insert(
                    0, "Region", [region] * len(combine_data["Benefit cause"])
                )
                compiled_discount0.insert(
                    0, "Package", [package] * len(combine_data["Benefit cause"])
                )
                compiled_discount_df = pd.concat(
                    [compiled_discount_df, compiled_discount0]
                )

            stillbirth_totals = []
            for stillbirth_prop in [
                0.25,
                pars_country["Intrapartum stillbirth proportion"][0],
                1,
            ]:
                orig = pars_country["Intrapartum stillbirth proportion"][0]
                pars_country["Intrapartum stillbirth proportion"] = stillbirth_prop
                benefits = total_econ_benefits(
                    pars_country,
                    preg_avert,
                    mat_death,
                    mat_morb,
                    neo_death,
                    neo_morb,
                    child_death,
                    child_morb,
                    stillbirth,
                    start_year=2022,
                    end_year=final_year,
                    include_fp_stillbirth_mort=include_fp_stillbirth_mort,
                )
                stillbirth_totals.append(benefits)
                pars_country["Intrapartum stillbirth proportion"] = orig
            total_data = {
                "Proportion of stillbirths counted: "
                + str(round(discount, 3))
                + ", Benefits": stillbirth_totals[d]
                for d, discount in enumerate(
                    [0.25, pars_country["Intrapartum stillbirth proportion"][0], 1]
                )
            }
            combine_data = {**label_data, **total_data}
            if r == 0 and p == 0:
                compiled_stillbirth_df = pd.DataFrame(data=combine_data)
                compiled_stillbirth_df.insert(
                    0, "Region", [region] * len(combine_data["Benefit cause"])
                )
                compiled_stillbirth_df.insert(
                    0, "Package", [package] * len(combine_data["Benefit cause"])
                )
            else:
                compiled_stillbirth0 = pd.DataFrame(data=combine_data)
                compiled_stillbirth0.insert(
                    0, "Region", [region] * len(combine_data["Benefit cause"])
                )
                compiled_stillbirth0.insert(
                    0, "Package", [package] * len(combine_data["Benefit cause"])
                )
                compiled_stillbirth_df = pd.concat(
                    [compiled_stillbirth_df, compiled_stillbirth0]
                )

            edu_increase_totals = []
            for edu_increase in [
                0,
                pars_country["Education gain due to teenage pregnancy averted"][0],
                2,
            ]:
                orig = pars_country["Education gain due to teenage pregnancy averted"][
                    0
                ]
                pars_country[
                    "Education gain due to teenage pregnancy averted"
                ] = edu_increase
                benefits = total_econ_benefits(
                    pars_country,
                    preg_avert,
                    mat_death,
                    mat_morb,
                    neo_death,
                    neo_morb,
                    child_death,
                    child_morb,
                    stillbirth,
                    start_year=2022,
                    end_year=final_year,
                    include_fp_stillbirth_mort=include_fp_stillbirth_mort,
                )
                edu_increase_totals.append(benefits)
                pars_country["Education gain due to teenage pregnancy averted"] = orig

            total_data = {
                "Years of education increase assumed: "
                + str(round(discount, 2))
                + ", Benefits": edu_increase_totals[d]
                for d, discount in enumerate(
                    [
                        0,
                        pars_country["Education gain due to teenage pregnancy averted"][
                            0
                        ],
                        2,
                    ]
                )
            }
            combine_data = {**label_data, **total_data}
            if r == 0 and p == 0:
                compiled_education_df = pd.DataFrame(data=combine_data)
                compiled_education_df.insert(
                    0, "Region", [region] * len(combine_data["Benefit cause"])
                )
                compiled_education_df.insert(
                    0, "Package", [package] * len(combine_data["Benefit cause"])
                )
            else:
                compiled_education0 = pd.DataFrame(data=combine_data)
                compiled_education0.insert(
                    0, "Region", [region] * len(combine_data["Benefit cause"])
                )
                compiled_education0.insert(
                    0, "Package", [package] * len(combine_data["Benefit cause"])
                )
                compiled_education_df = pd.concat(
                    [compiled_education_df, compiled_education0]
                )

            work_time_totals = []
            for work_time in [
                0,
                pars_country["Maternal time out of workforce"][0],
                0.5,
            ]:
                orig = pars_country["Maternal time out of workforce"][0]
                pars_country["Maternal time out of workforce"] = work_time
                benefits = total_econ_benefits(
                    pars_country,
                    preg_avert,
                    mat_death,
                    mat_morb,
                    neo_death,
                    neo_morb,
                    child_death,
                    child_morb,
                    stillbirth,
                    start_year=2022,
                    end_year=final_year,
                    include_fp_stillbirth_mort=include_fp_stillbirth_mort,
                )
                work_time_totals.append(benefits)
                pars_country["Maternal time out of workforce"] = orig

            total_data = {
                "Years of additional work assumed: "
                + str(round(discount, 2))
                + ", Benefits": work_time_totals[d]
                for d, discount in enumerate(
                    [0, pars_country["Maternal time out of workforce"][0], 0.5]
                )
            }
            combine_data = {**label_data, **total_data}
            if r == 0 and p == 0:
                compiled_worktime_df = pd.DataFrame(data=combine_data)
                compiled_worktime_df.insert(
                    0, "Region", [region] * len(combine_data["Benefit cause"])
                )
                compiled_worktime_df.insert(
                    0, "Package", [package] * len(combine_data["Benefit cause"])
                )
            else:
                compiled_worktime0 = pd.DataFrame(data=combine_data)
                compiled_worktime0.insert(
                    0, "Region", [region] * len(combine_data["Benefit cause"])
                )
                compiled_worktime0.insert(
                    0, "Package", [package] * len(combine_data["Benefit cause"])
                )
                compiled_worktime_df = pd.concat(
                    [compiled_worktime_df, compiled_worktime0]
                )

            life_year_totals = []
            for life_year in [0, pars_country["Social_value"][0], 1]:
                orig = pars_country["Social_value"][0]
                pars_country["Social_value"] = life_year
                benefits = total_econ_benefits(
                    pars_country,
                    preg_avert,
                    mat_death,
                    mat_morb,
                    neo_death,
                    neo_morb,
                    child_death,
                    child_morb,
                    stillbirth,
                    start_year=2022,
                    end_year=final_year,
                    include_fp_stillbirth_mort=include_fp_stillbirth_mort,
                )
                life_year_totals.append(benefits)
                pars_country["Social_value"] = orig

            total_data = {
                "Value of statistical life year: "
                + str(round(discount, 2))
                + ", Benefits": life_year_totals[d]
                for d, discount in enumerate([0, pars_country["Social_value"][0], 1])
            }
            combine_data = {**label_data, **total_data}
            if r == 0 and p == 0:
                compiled_life_year_df = pd.DataFrame(data=combine_data)
                compiled_life_year_df.insert(
                    0, "Region", [region] * len(combine_data["Benefit cause"])
                )
                compiled_life_year_df.insert(
                    0, "Package", [package] * len(combine_data["Benefit cause"])
                )
            else:
                compiled_life_year0 = pd.DataFrame(data=combine_data)
                compiled_life_year0.insert(
                    0, "Region", [region] * len(combine_data["Benefit cause"])
                )
                compiled_life_year0.insert(
                    0, "Package", [package] * len(combine_data["Benefit cause"])
                )
                compiled_life_year_df = pd.concat(
                    [compiled_life_year_df, compiled_life_year0]
                )

            earning_totals = []
            for earn_benefit in [0.03, pars_country["Education benefit"][0], 0.35]:
                orig = pars_country["Education benefit"][0]
                pars_country["Education benefit"] = earn_benefit
                benefits = total_econ_benefits(
                    pars_country,
                    preg_avert,
                    mat_death,
                    mat_morb,
                    neo_death,
                    neo_morb,
                    child_death,
                    child_morb,
                    stillbirth,
                    start_year=2022,
                    end_year=final_year,
                    include_fp_stillbirth_mort=include_fp_stillbirth_mort,
                )
                earning_totals.append(benefits)
                pars_country["Education benefit"] = orig

            total_data = {
                "Earning increase from year of additional education: "
                + str(round(discount, 2))
                + ", Benefits": earning_totals[d]
                for d, discount in enumerate(
                    [0.03, pars_country["Education benefit"][0], 0.35]
                )
            }
            combine_data = {**label_data, **total_data}
            if r == 0 and p == 0:
                compiled_edu_benefit_df = pd.DataFrame(data=combine_data)
                compiled_edu_benefit_df.insert(
                    0, "Region", [region] * len(combine_data["Benefit cause"])
                )
                compiled_edu_benefit_df.insert(
                    0, "Package", [package] * len(combine_data["Benefit cause"])
                )
            else:
                compiled_edu_benefit0 = pd.DataFrame(data=combine_data)
                compiled_edu_benefit0.insert(
                    0, "Region", [region] * len(combine_data["Benefit cause"])
                )
                compiled_edu_benefit0.insert(
                    0, "Package", [package] * len(combine_data["Benefit cause"])
                )
                compiled_edu_benefit_df = pd.concat(
                    [compiled_edu_benefit_df, compiled_edu_benefit0]
                )

            wage_totals = []
            for wage in [
                0.75 * pars_country["Average annual salary"][0],
                pars_country["Average annual salary"][0],
                1.25 * pars_country["Average annual salary"][0],
            ]:
                orig = pars_country["Average annual salary"][0]
                pars_country["Average annual salary"] = wage
                benefits = total_econ_benefits(
                    pars_country,
                    preg_avert,
                    mat_death,
                    mat_morb,
                    neo_death,
                    neo_morb,
                    child_death,
                    child_morb,
                    stillbirth,
                    start_year=2022,
                    end_year=final_year,
                    include_fp_stillbirth_mort=include_fp_stillbirth_mort,
                )
                wage_totals.append(benefits)
                pars_country["Average annual salary"] = orig

            total_data = {
                "Average wage: "
                + str(round(discount, 2))
                + ", Benefits": wage_totals[d]
                for d, discount in enumerate([0.75, 1, 1.25])
            }
            combine_data = {**label_data, **total_data}
            if r == 0 and p == 0:
                compiled_average_wage_df = pd.DataFrame(data=combine_data)
                compiled_average_wage_df.insert(
                    0, "Region", [region] * len(combine_data["Benefit cause"])
                )
                compiled_average_wage_df.insert(
                    0, "Package", [package] * len(combine_data["Benefit cause"])
                )
            else:
                compiled_average_wage0 = pd.DataFrame(data=combine_data)
                compiled_average_wage0.insert(
                    0, "Region", [region] * len(combine_data["Benefit cause"])
                )
                compiled_average_wage0.insert(
                    0, "Package", [package] * len(combine_data["Benefit cause"])
                )
                compiled_average_wage_df = pd.concat(
                    [compiled_average_wage_df, compiled_average_wage0]
                )

            final_year_totals = []
            for final_year_new in [2030, 2050, 2070]:
                benefits = total_econ_benefits(
                    pars_country,
                    preg_avert,
                    mat_death,
                    mat_morb,
                    neo_death,
                    neo_morb,
                    child_death,
                    child_morb,
                    stillbirth,
                    start_year=2022,
                    end_year=final_year_new,
                    include_fp_stillbirth_mort=include_fp_stillbirth_mort,
                )
                final_year_totals.append(benefits)

            total_data = {
                "Benefits counted until: "
                + str(round(discount, 2))
                + ", Benefits": final_year_totals[d]
                for d, discount in enumerate([2030, 2050, 2070])
            }
            combine_data = {**label_data, **total_data}
            if r == 0 and p == 0:
                compiled_final_year_df = pd.DataFrame(data=combine_data)
                compiled_final_year_df.insert(
                    0, "Region", [region] * len(combine_data["Benefit cause"])
                )
                compiled_final_year_df.insert(
                    0, "Package", [package] * len(combine_data["Benefit cause"])
                )
            else:
                compiled_final_year0 = pd.DataFrame(data=combine_data)
                compiled_final_year0.insert(
                    0, "Region", [region] * len(combine_data["Benefit cause"])
                )
                compiled_final_year0.insert(
                    0, "Package", [package] * len(combine_data["Benefit cause"])
                )
                compiled_final_year_df = pd.concat(
                    [compiled_final_year_df, compiled_final_year0]
                )

            teen_preg_totals = []
            for teen_prop in [
                0.5 * pars_country["Proportion of PW 15-19 yo"][0],
                pars_country["Proportion of PW 15-19 yo"][0],
                2 * pars_country["Proportion of PW 15-19 yo"][0],
            ]:

                orig1 = pars_country["Proportion of PW 15-19 yo"][0]
                orig2 = pars_country["Proportion of PW 20-24 yo"][0]
                orig3 = pars_country["Proportion of PW 25-29 yo"][0]
                orig4 = pars_country["Proportion of PW 30-34 yo"][0]
                orig5 = pars_country["Proportion of PW 35-39 yo"][0]
                orig6 = pars_country["Proportion of PW 40-44 yo"][0]
                orig7 = pars_country["Proportion of PW 45-49 yo"][0]
                pars_country["Proportion of PW 15-19 yo"] = teen_prop
                pars_country["Proportion of PW 20-24 yo"] = pars_country[
                    "Proportion of PW 20-24 yo"
                ][0] - (teen_prop - orig1) * (5 / 31)
                pars_country["Proportion of PW 25-29 yo"] = pars_country[
                    "Proportion of PW 25-29 yo"
                ][0] - (teen_prop - orig1) * (5 / 31)
                pars_country["Proportion of PW 30-34 yo"] = pars_country[
                    "Proportion of PW 30-34 yo"
                ][0] - (teen_prop - orig1) * (5 / 31)
                pars_country["Proportion of PW 35-39 yo"] = pars_country[
                    "Proportion of PW 35-39 yo"
                ][0] - (teen_prop - orig1) * (5 / 31)
                pars_country["Proportion of PW 35-39 yo"] = pars_country[
                    "Proportion of PW 35-39 yo"
                ][0] - (teen_prop - orig1) * (5 / 31)
                pars_country["Proportion of PW 35-39 yo"] = pars_country[
                    "Proportion of PW 35-39 yo"
                ][0] - (teen_prop - orig1) * (5 / 31)

                benefits = total_econ_benefits(
                    pars_country,
                    preg_avert,
                    mat_death,
                    mat_morb,
                    neo_death,
                    neo_morb,
                    child_death,
                    child_morb,
                    stillbirth,
                    start_year=2022,
                    end_year=final_year_new,
                    include_fp_stillbirth_mort=include_fp_stillbirth_mort,
                )
                teen_preg_totals.append(benefits)
                pars_country["Proportion of PW 15-19 yo"] = orig1
                pars_country["Proportion of PW 20-24 yo"] = orig2
                pars_country["Proportion of PW 25-29 yo"] = orig3
                pars_country["Proportion of PW 30-34 yo"] = orig4
                pars_country["Proportion of PW 35-39 yo"] = orig5
                pars_country["Proportion of PW 40-44 yo"] = orig6
                pars_country["Proportion of PW 45-49 yo"] = orig7

            total_data = {
                "Proportion of averted pregnancies in teenage girls: "
                + discount
                + ", Benefits": teen_preg_totals[d]
                for d, discount in enumerate(["Zero", "Baseline", "Double"])
            }
            combine_data = {**label_data, **total_data}
            if r == 0 and p == 0:
                compiled_teen_preg_df = pd.DataFrame(data=combine_data)
                compiled_teen_preg_df.insert(
                    0, "Region", [region] * len(combine_data["Benefit cause"])
                )
                compiled_teen_preg_df.insert(
                    0, "Package", [package] * len(combine_data["Benefit cause"])
                )
            else:
                compiled_teen_preg0 = pd.DataFrame(data=combine_data)
                compiled_teen_preg0.insert(
                    0, "Region", [region] * len(combine_data["Benefit cause"])
                )
                compiled_teen_preg0.insert(
                    0, "Package", [package] * len(combine_data["Benefit cause"])
                )
                compiled_teen_preg_df = pd.concat(
                    [compiled_teen_preg_df, compiled_teen_preg0]
                )

            GDP_growth_totals = []
            for GDP_growth in [0, pars_country["Annual GDP growth"][0], 0.05]:
                orig = pars_country["Annual GDP growth"][0]
                pars_country["Annual GDP growth"] = GDP_growth
                benefits = total_econ_benefits(
                    pars_country,
                    preg_avert,
                    mat_death,
                    mat_morb,
                    neo_death,
                    neo_morb,
                    child_death,
                    child_morb,
                    stillbirth,
                    start_year=2022,
                    end_year=final_year,
                    include_fp_stillbirth_mort=include_fp_stillbirth_mort,
                )
                GDP_growth_totals.append(benefits)
                pars_country["Annual GDP growth"] = orig

            total_data = {
                "Annual GDP growth: "
                + str(round(discount, 2))
                + ", Benefits": GDP_growth_totals[d]
                for d, discount in enumerate(
                    [0, pars_country["Annual GDP growth"][0], 1]
                )
            }
            combine_data = {**label_data, **total_data}
            if r == 0 and p == 0:
                compiled_GDP_growth_df = pd.DataFrame(data=combine_data)
                compiled_GDP_growth_df.insert(
                    0, "Region", [region] * len(combine_data["Benefit cause"])
                )
                compiled_GDP_growth_df.insert(
                    0, "Package", [package] * len(combine_data["Benefit cause"])
                )
            else:
                compiled_GDP_growth0 = pd.DataFrame(data=combine_data)
                compiled_GDP_growth0.insert(
                    0, "Region", [region] * len(combine_data["Benefit cause"])
                )
                compiled_GDP_growth0.insert(
                    0, "Package", [package] * len(combine_data["Benefit cause"])
                )
                compiled_GDP_growth_df = pd.concat(
                    [compiled_GDP_growth_df, compiled_GDP_growth0]
                )

    sens_set = [
        compiled_discount_df,
        compiled_stillbirth_df,
        compiled_education_df,
        compiled_worktime_df,
        compiled_life_year_df,
        compiled_edu_benefit_df,
        compiled_average_wage_df,
        compiled_final_year_df,
        compiled_teen_preg_df,
        compiled_GDP_growth_df,
    ]

    if include_all_countries:
        print("all countries calcs")

        for s in range(len(sens_set)):
            totals = (
                sens_set[s]
                .groupby(["Benefit cause"])
                .sum(numeric_only=True)
                .reset_index()
            )
            region = "All countries"
            totals.loc[
                totals["Benefit cause"] == "Total BCR",
                totals.columns != "Benefit cause",
            ] = (
                totals.loc[
                    totals["Benefit cause"] == "Total benefit",
                    totals.columns != "Benefit cause",
                ].values
                / total_cost
            )
            totals.loc[
                totals["Benefit cause"] == "Labour % of benefits",
                totals.columns != "Benefit cause",
            ] = (
                totals.loc[totals["Benefit cause"] == "Total work benefits"]
                .iloc[0, 1:]
                .values
                / totals.loc[totals["Benefit cause"] == "Total benefit"]
                .iloc[0, 1:]
                .values
            )
            totals.loc[
                totals["Benefit cause"] == "Education % of benefits",
                totals.columns != "Benefit cause",
            ] = (
                totals.loc[totals["Benefit cause"] == "Total education benefits"]
                .iloc[0, 1:]
                .values
                / totals.loc[totals["Benefit cause"] == "Total benefit"]
                .iloc[0, 1:]
                .values
            )
            totals.loc[
                totals["Benefit cause"] == "Social % of benefits",
                totals.columns != "Benefit cause",
            ] = (
                totals.loc[totals["Benefit cause"] == "Total social benefits"]
                .iloc[0, 1:]
                .values
                / totals.loc[totals["Benefit cause"] == "Total benefit"]
                .iloc[0, 1:]
                .values
            )
            totals.insert(0, "Region", region)
            totals.insert(0, "Package", package)
            sens_set[s] = pd.concat([totals, sens_set[s]])

    """ Creation of the output file, changing the name structure will mess up the linked summary plot files!! """
    if output_to_excel:
        writer = pd.ExcelWriter(output_filepath, engine="xlsxwriter")
        main_results.to_excel(writer, sheet_name="Main results", index=False)
        sens_set[0].to_excel(writer, sheet_name="Varying discount rate", index=False)
        sens_set[1].to_excel(
            writer, sheet_name="Varying stillbirth counting", index=False
        )
        sens_set[2].to_excel(
            writer, sheet_name="Varying education increase", index=False
        )
        sens_set[3].to_excel(
            writer, sheet_name="Varying worktime increase", index=False
        )
        sens_set[4].to_excel(writer, sheet_name="Varying stat life year", index=False)
        sens_set[5].to_excel(
            writer, sheet_name="Varying education benefit", index=False
        )
        sens_set[6].to_excel(writer, sheet_name="Varying average wage", index=False)
        sens_set[7].to_excel(
            writer, sheet_name="Varying year benefits tracked", index=False
        )
        sens_set[8].to_excel(
            writer, sheet_name="Varying teen preg averted", index=False
        )
        sens_set[9].to_excel(
            writer, sheet_name="Varying annual GDP growth", index=False
        )
        daly_df.to_excel(writer, sheet_name="DALYs", index=False)
        writer.close()

    collated_results = collate_results(
        [
            "Main results",
            "Varying discount rate",
            "Varying stillbirth counting",
            "Varying education increase",
            "Varying worktime increase",
            "Varying stat life year",
            "Varying education benefit",
            "Varying average wage",
            "Varying year benefits tracked",
            "Varying teen preg averted",
            "Varying annual GDP growth",
            "DALYs",
        ],
        main_results,
        sens_set,
        daly_df,
    )

    print("Finished sensitivity analysis!")

    return collated_results
