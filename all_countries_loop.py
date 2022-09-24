import numpy as np
import pandas as pd
from calc_benefit_types import *
from population_structure import *
np.seterr(divide='ignore', invalid='ignore')

def read_benefit_params(country, filepath):
    """
    Pull in parameters to be used in benefit cost calculations
      :param country: country or region to be extracted, corresponding to rows in the excel workbook
      :param filepath: location of file with BCR input template
      :param include_fp_mort: determines whether stillbirths, neonatal deaths and child deaths averted due to pregnancies averted are included
      :return: parameters for BCR calculations and vectors for deaths etc to be used in calculations
    """

    maternal_lives_saved = pd.read_excel(filepath, sheet_name='Mat lives saved')
    neonatal_lives_saved = pd.read_excel(filepath, sheet_name = 'Neo lives saved')
    stillbirths_averted = pd.read_excel(filepath, sheet_name = 'Stillbirths averted')
    unintended_preg_avert = pd.read_excel(filepath, sheet_name='Unintended pregnancies averted')
    child_lives_saved = pd.read_excel(filepath, sheet_name='Child lives saved')
    fp_maternal_lives_saved = pd.read_excel(filepath, sheet_name='FP_Mat lives saved')
    maternal_morbidities_averted = pd.read_excel(filepath, sheet_name='Mat morbidities averted')
    neo_morbidities_averted = pd.read_excel(filepath, sheet_name='Neo morbidites averted')
    wasting_averted = pd.read_excel(filepath, sheet_name='Wasting averted')
    stunting_averted = pd.read_excel(filepath, sheet_name='Stunting averted')

    mat_death = np.array(maternal_lives_saved.loc[maternal_lives_saved['Country'] == country, 2022:2030])
    mat_death = np.nan_to_num(mat_death).flatten()
    child_death = np.array(child_lives_saved.loc[child_lives_saved['Country'] == country, 2022:2030])
    child_death = np.nan_to_num(child_death).flatten()
    neo_death = np.array(neonatal_lives_saved.loc[neonatal_lives_saved['Country'] == country, 2022:2030])
    neo_death = np.nan_to_num(neo_death).flatten()
    stillbirth = np.array(stillbirths_averted.loc[stillbirths_averted['Country'] == country, 2022:2030])
    stillbirth = np.nan_to_num(stillbirth).flatten()
    preg_avert = np.array(unintended_preg_avert.loc[unintended_preg_avert['Country'] == country, 2022:2030])
    preg_avert = np.nan_to_num(preg_avert).flatten()

    #FP deaths averted
    fp_mat_death = np.array(fp_maternal_lives_saved.loc[fp_maternal_lives_saved['Country'] == country, 2022:2030])
    fp_mat_death = np.nan_to_num(fp_mat_death).flatten()
    #Add FP maternal deaths to maternal deaths
    mat_death = mat_death + fp_mat_death

    # Morbidities
    mat_morb = {}
    child_morb = {}
    neo_morb = {}
    mat_morb0 = np.array(maternal_morbidities_averted.loc[maternal_morbidities_averted['Country'] == country, 2022:2030])
    mat_morb['YLD'] = np.nan_to_num(mat_morb0).flatten()
    child_morb0 = np.array(wasting_averted.loc[wasting_averted['Country'] == country, 2022:2030])
    child_morb['Wasting'] = np.nan_to_num(child_morb0).flatten()
    child_morb0 = np.array(stunting_averted.loc[wasting_averted['Country'] == country, 2022:2030])
    child_morb['Stunting'] = np.nan_to_num(child_morb0).flatten()
    neo_morb0 = np.array(neo_morbidities_averted.loc[neo_morbidities_averted['Country'] == country, 2022:2030])
    neo_morb['General'] = np.nan_to_num(neo_morb0).flatten()


    constant_params = pd.read_excel(filepath, sheet_name='BCR inputs constant')
    pars_country = constant_params.loc[constant_params['Country'] == country].reset_index()

    return pars_country, preg_avert, mat_death, mat_morb, neo_death, neo_morb, child_death, child_morb, stillbirth


def total_econ_benefits(pars_country, preg_avert, mat_death, mat_morb, neo_death, neo_morb, child_death,
                        child_morb, stillbirth, start_year=2022, end_year=2030, include_fp_stillbirth_mort=False):
    """
    :param pars_country: Dataframe with parameters for specific country or setting
    :param preg_avert: Vector of pregnancies averted per year
    :param mat_death:
    :param mat_morb:
    :param neo_death:
    :param neo_morb:
    :param child_death:
    :param child_morb:
    :param stillbirth:
    :param time_limit:
    :param start_year:
    :param end_year:
    :return:
    """

    population_mat_death, population_child_death, population_neo_death, population_stillbirth, population_preg_averted_labour, \
    population_preg_averted_education = population_structure(pars_country, mat_death, child_death, neo_death, stillbirth,
                                                             preg_avert, start_year=start_year, end_year=end_year, include_fp_stillbirth_mort=include_fp_stillbirth_mort)

    '''Social benefits'''
    # Transform DALYs averted in social economic benefit
    dalys_mat_death = calc_daly_annual(population_mat_death, pars_country, start_year=start_year, end_year=end_year)
    dalys_child_death = calc_daly_annual(population_child_death, pars_country, start_year=start_year, end_year=end_year)
    dalys_neo_death = calc_daly_annual(population_neo_death, pars_country, start_year=start_year, end_year=end_year)
    dalys_stillbirth = calc_daly_annual(population_stillbirth, pars_country, start_year=start_year, end_year=end_year)

    dalys_YLD = calc_YLD(pars_country, mat_morb, neo_morb, child_morb, start_year=start_year, end_year=end_year)

    social_econ_benefits = dalys_mat_death + dalys_child_death + dalys_neo_death + dalys_stillbirth + dalys_YLD

    '''Labour force benefits'''
    # Calculate labour force benefits
    work_benefits_mat_mort = calc_work_benefits(population_mat_death, pars_country, work_participation=pars_country['Proportion of women who participate in workforce'][0],
                                                prop_year=1, start_year=start_year, end_year=end_year)
    work_benefits_preg_avert = calc_work_benefits(population_preg_averted_labour, pars_country, work_participation=pars_country['Proportion of women who participate in workforce'][0],
                                                  prop_year=pars_country['Maternal time out of workforce'][0], start_year=start_year, end_year=end_year)
    work_benefits_child_mort = calc_work_benefits(population_child_death, pars_country, work_participation=pars_country['Workforce participation'][0],
                                                  prop_year=1, start_year=start_year, end_year=end_year)
    work_benefits_neo_mort = calc_work_benefits(population_neo_death, pars_country, work_participation=pars_country['Workforce participation'][0],
                                                prop_year=1, start_year=start_year, end_year=end_year)
    work_benefits_stillbirth = calc_work_benefits(population_stillbirth, pars_country, work_participation=pars_country['Workforce participation'][0],
                                                  prop_year=1, start_year=start_year, end_year=end_year)
    work_econ_benefits = work_benefits_mat_mort + work_benefits_preg_avert +  work_benefits_child_mort + work_benefits_neo_mort + work_benefits_stillbirth

    '''Education benefits'''
    #Calculate education benefits
    edu_econ_benefits = calc_education_benefits(population_preg_averted_education, pars_country, end_year=end_year, start_year=start_year)

    # Ensure that the length of economic benefit vectors match
    if len(social_econ_benefits) < len(edu_econ_benefits):
        social_econ_benefits = np.append(social_econ_benefits, np.zeros([len(edu_econ_benefits) - len(social_econ_benefits), len(social_econ_benefits)]), axis=0)
    elif len(social_econ_benefits) > len(edu_econ_benefits): # If necessary remove start year
        social_econ_benefits = np.delete(social_econ_benefits, 0, 0)

    '''Economic benefits output '''
    # Total economic benefit from scale up
    sum_econ_benefits = sum(social_econ_benefits) + sum(work_econ_benefits) + sum(edu_econ_benefits)

    # Economic benefits due to different 'results'
    maternal_death_benefits = sum(dalys_mat_death) + sum(work_benefits_mat_mort)
    neonatal_death_benefits = sum(dalys_neo_death) + sum(work_benefits_neo_mort)
    child_death_benefits = sum(dalys_child_death) + sum(work_benefits_child_mort)# Including HIV disabilities
    stillbirth_benefits = sum(dalys_stillbirth) + sum(work_benefits_stillbirth)
    teen_preg_avert_edu_benefits = sum(edu_econ_benefits)
    preg_avert_work_benefits = sum(work_benefits_preg_avert)
    work_benefits_tot = sum(work_econ_benefits)
    social_benefits_tot = sum(social_econ_benefits)
    edu_benefits_tot = sum(edu_econ_benefits)

    BCR = sum_econ_benefits / pars_country['Total expenditure'][0]
    labour_benefits = sum(work_econ_benefits) / sum_econ_benefits * 100
    social_benefits = sum(social_econ_benefits) / sum_econ_benefits * 100
    edu_econ_benefits = sum(edu_econ_benefits) / sum_econ_benefits * 100

    return (sum_econ_benefits, maternal_death_benefits, neonatal_death_benefits, child_death_benefits, stillbirth_benefits,
            teen_preg_avert_edu_benefits, preg_avert_work_benefits, work_benefits_tot, edu_benefits_tot, social_benefits_tot,
            BCR, labour_benefits, edu_econ_benefits, social_benefits)


def run_bcr_script(region_list, inpath, outpath, final_year, include_fp_stillbirth_mort = True):

    '''
    :param: region_List: List of regions considered in the analysis (can be country name if it is a national analysis only.)
    :param inpath: file path for BCR input file (most likely summary sheet)
    :param outpath: file path for BCR outputs
    '''

    #filepath, initials = ou._get_gdrive_folder()
    input_filepath = inpath
    output_filepath = outpath
    standard_benefits_total = [0]
    total_cost = [0]

    for r, region in enumerate(region_list):
        for p, package in enumerate(['']):
            pars_country, preg_avert, mat_death, mat_morb, neo_death, neo_morb, child_death, child_morb, stillbirth \
                = read_benefit_params(region, input_filepath)

            standard_benefits = total_econ_benefits(pars_country, preg_avert, mat_death, mat_morb, neo_death, neo_morb,
                                                    child_death, child_morb, stillbirth, start_year = 2022, end_year=final_year, include_fp_stillbirth_mort=include_fp_stillbirth_mort)
            standard_benefits_total = standard_benefits_total + standard_benefits[0]
            total_cost = total_cost + pars_country['Total expenditure'][0]

            # Summarize
            label_data = {'Benefit cause': ['Total benefit', 'Maternal death averted benefit', 'Neonatal death averted benefit', 'Child death averted benefit',
                                            'Stillbirth averted benefit', 'Teenage pregnancy averted education benefit',
                                            'Pregnancy averted work benefit', 'Total work benefits', 'Total education benefits', 'Total social benefits',
                                            'Total BCR', 'Labour % of benefits', 'Education % of benefits', 'Social % of benefits']}
            label_data = {'Benefit cause': [ben for ben in label_data['Benefit cause']]}
            total_data = {'Outcomes': standard_benefits}
            combine_data = {**label_data, **total_data}
            if r == 0 and p == 0:
                main_results_df = pd.DataFrame(data=combine_data)
                main_results_df.insert(0, 'Region', [region] * len(combine_data['Benefit cause']))
                main_results_df.insert(0, 'Package', [package] * len(combine_data['Benefit cause']))
            else:
                main_results0 = pd.DataFrame(data=combine_data)
                main_results0.insert(0, 'Region', [region] * len(combine_data['Benefit cause']))
                main_results0.insert(0, 'Package', [package] * len(combine_data['Benefit cause']))
                main_results_df = pd.concat([main_results_df, main_results0])


            dalys = calc_daly(pars_country, mat_death, mat_morb, neo_death, neo_morb, child_death, child_morb, stillbirth)
            dalys = list(map(list, zip(*dalys)))
            label_data = {'Year': list(range(2022, 2031))}
            label_data = {'Year': [region + package + ' ' + str(year) for year in label_data['Year']]}
            total_data = {'Neonatal YLLs': dalys[0], 'Child YLLs': dalys[1], 'Maternal YLLs': dalys[2],
                       'Stillbirth YLLs': dalys[3], 'Neonatal DALYs': dalys[4], 'Child DALYs': dalys[5],
                       'Maternal DALYs': dalys[6], 'Total YLLs': dalys[7], 'Total DALYs': dalys[8], 'Total': dalys[9]}
            daly_data = {**label_data, **total_data}
            if r == 0 and p == 0:
                daly_df = pd.DataFrame(data=daly_data)
            else:
                daly_df = pd.concat([daly_df, pd.DataFrame(data=daly_data)])
            print(region)
            print('Total BCR: %0.1f'  % standard_benefits[10])
            print('Labour BCR: %0.1f percent of total benefits' % standard_benefits[11])
            print('Education BCR: %0.1f percent of total benefits' % standard_benefits[12])
            print('Social BCR: %0.1f percent of total benefits' % standard_benefits[13])

    print('Finished!')
    totals = main_results_df.groupby(['Benefit cause']).sum().reset_index()
    total_bcr = standard_benefits_total / total_cost
    print('All country BCR: %0.1f' % total_bcr)
    region = 'All countries'
    totals.insert(0,'Region', region)
    totals.insert(0, 'Package', package)
    totals.loc[totals['Benefit cause'] =='Total BCR',['Outcomes']] = totals.loc[totals['Benefit cause'] =='Total benefit']['Outcomes'].values / total_cost
    totals.loc[totals['Benefit cause'] == 'Labour % of benefits', ['Outcomes']] \
        = totals.loc[totals['Benefit cause'] == 'Total work benefits']['Outcomes'].values / \
          totals.loc[totals['Benefit cause'] =='Total benefit']['Outcomes'].values
    totals.loc[totals['Benefit cause'] == 'Education % of benefits', ['Outcomes']] \
        = totals.loc[totals['Benefit cause'] == 'Total education benefits']['Outcomes'].values / \
          totals.loc[totals['Benefit cause'] == 'Total benefit']['Outcomes'].values
    totals.loc[totals['Benefit cause'] == 'Social % of benefits', ['Outcomes']] \
        = totals.loc[totals['Benefit cause'] == 'Total social benefits']['Outcomes'].values / \
          totals.loc[totals['Benefit cause'] == 'Total benefit']['Outcomes'].values

    main_results_df = pd.concat([totals, main_results_df])
    return main_results_df, daly_df

