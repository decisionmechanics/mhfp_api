import numpy as np
from population_structure import *

def calc_education_benefits(input_population, pars_country, start_year = 2022, end_year = 2030):
    '''
    :param input_population: Vector of population inputs by year
    :param pars_country: Dataframe with parameters for specific country or setting
    :param start_year: First year of projected benefits
    :param end_year: Final year of projected benefits
    :return:
    '''
    years = list(range(0, end_year - start_year + 1))
    # Earning multipliers for longer educated worker/worker/non-worker
    earn_mult = pars_country['Education gain due to teenage pregnancy averted'][0] * pars_country['Education benefit'][0]
    edu_workers_earnings = np.zeros((len(years)))

    # Sum all the years of additional wages among those with more education, from working age categories
    for year in years:
        edu_workers_earnings[year] = np.sum(input_population[year, 18:64] * earn_mult) * pars_country['Average annual salary'][0] \
                                     * pars_country['Proportion of women who participate in workforce'][0] \
                                     * (1 + pars_country['Annual GDP growth'][0]) ** (year + 2) \
                                     * (1 / (1 + pars_country['Discounting'][0]) ** (year+2)) # 2020 is year 0

    return edu_workers_earnings

def calc_work_benefits(input_population, pars_country, work_participation, prop_year=1,  start_year=2022, end_year=2030):
    '''
    :param input_population: Vector of pregnancies averted per year, or deaths averted per year, for calculations
    :param pars_country: Dataframe with parameters for specific country or setting
    :param prop_year: assumption about fraction of year missing from workforce
    :param work_participation: workforce participation among input population
    :param start_year: First year of projected benefits
    :param end_year: Final year of projected benefits
    :return:
    '''
    years = list(range(0, end_year - start_year + 1))
    workers_earnings = np.zeros((len(years)))
    for year in years:
        workers_earnings[year] = sum(input_population[year, 18:64]) * work_participation * pars_country['Average annual salary'][0] \
                                 * (1 + pars_country['Annual GDP growth'][0]) ** (year + 2) \
                                 * prop_year * (1 / (1 + pars_country['Discounting'][0]) ** (year+2)) # 2020 is year 0

    return workers_earnings


def calc_daly_annual(input_population, pars_country, start_year=2022, end_year=2030):
    '''
    :param input_population: Vector of pregnancies averted per year, or deaths averted per year, for calculations
    :param pars_country: Dataframe with parameters for specific country or setting
    :param start_year: First year of projected benefits
    :param end_year: Final year of projected benefits
    :return:
    '''

    years = list(range(0, end_year - start_year + 1))
    daly_benefit = np.zeros((len(years)))
    for year in years:
        daly_benefit[year] = sum(input_population[year, :]) * pars_country['Social_value'][0] \
                             * pars_country['GDP per capita weighted'][0] \
                             * (1 + pars_country['Annual GDP growth'][0]) ** (year + 2) \
                             * (1 / (1 + pars_country['Discounting'][0]) ** (year+2)) # 2020 is year 0

    return daly_benefit

def calc_YLD(pars_country,mat_morb, neo_morb, child_morb, start_year=2022, end_year=2030):
    '''
    This function can be used if the DALYs are all to be attributed to the year that they were averted,
    rather than attributing them to the year that they would otherwise have lived
    :param pars_country: Dataframe with parameters for specific country or setting
    :param mat_morb: A dictionary of vectors of maternal morbidities (HIV, STI, TB, etc.) averted per simulation year
    :param neo_morb: A dictionary of vectors of neonatal morbidities (HIV, preterm, LBW, etc.) averted per simulation year
    :param child_morb: A dictionary of vectors of child morbidities (HIV, preterm, LBW, etc.) averted per simulation year
    :return: A vector of DALYs averted per simulation year disaggregated by [neonatal YLLs, maternal YLLs, stillbirth YLLs,
             neonatal YLDs, maternal YLDs, total YLLs, total YLDs, total DALYs]
    '''

    # DALY weights for different conditions (proxy values) HIV from LiST assumptions
    mat_dw = {'YLD': 1, 'HIV': 0.33, 'STI': 0.21, 'TB': 0.25,  'General': 0.10}
    neo_dw = {'YLD': 1,'HIV': 0.221, 'Preterm': 0, 'LBW': 0,  'General': 0.10}
    child_dw = {'YLD': 1, 'Stunting': 0.66, 'Wasting': 0.128 * pars_country['Percent wasting severe'][0],  'General': 0.10}
    mat_dw_lifelong = {'YLD': False, 'HIV': True, 'STI': False, 'TB': True, 'General': False}  # Flags for whether these conditions are lifelong
    neo_dw_lifelong = {'YLD': False, 'HIV': True, 'Preterm': True, 'LBW': True, 'General': False}
    child_dw_lifelong = {'YLD': False, 'Stunting': True, 'Wasting': False}

    years = list(range(0, end_year - start_year + 1)) # time vector for how many years of health impacts / data are entered

    # Calculate YLD in for short term conditions. This section will be skipped if no disability data is entered
    daly_benefit = []
    for year in years:
        maternal_disability = 0
        neonatal_disability = 0
        child_disability = 0
        if bool(mat_morb):
            for d, disability in enumerate(mat_morb.keys()):
                if year < len(mat_morb[disability]):
                    if not neo_dw_lifelong[disability]:
                        maternal_disability += mat_morb[disability][year] * mat_dw[disability]
        if bool(neo_morb):
            for d, disability in enumerate(neo_morb.keys()):
                if year < len(neo_morb[disability]):
                    if not neo_dw_lifelong[disability]:
                        neonatal_disability += neo_morb[disability][year] * neo_dw[disability]
        if bool(child_morb):
            for d, disability in enumerate(child_morb.keys()):
                if year < len(child_morb[disability]):
                    if not child_dw_lifelong[disability]:
                        child_disability += child_morb[disability][year] * child_dw[disability]
        total_YLD = maternal_disability + neonatal_disability + child_disability
        YLD_eco = total_YLD * pars_country['Social_value'][0] * pars_country['GDP per capita weighted'][0] \
                  * (1 + pars_country['Annual GDP growth'][0]) ** (year + 2) \
                  * (1 / (1 + pars_country['Discounting'][0]) ** (year+2)) # 2020 is year 0
        daly_benefit.append(YLD_eco)

    # Calculate YLD in for permanent conditions. This section will be skipped if no disability data is entered
    maternal_disability_life = [0]*len(years)
    neonatal_disability_life = [0]*len(years)
    child_disability_life = [0]*len(years)
    for d, disability in enumerate(mat_morb.keys()):
        if mat_dw_lifelong[disability]:
            # Use ghost generating function to track the population of people with comorbidities over time
            p_mat_morbid, p_child_morbid, p_neo_morbid, p_stillbirth_morbid, p_preg_averted_labour, p_preg_averted_education \
                = population_structure(pars_country, mat_morb[disability], np.array([0]), np.array([0]), np.array([0]), np.array([0]), start_year=start_year, end_year=end_year,include_fp_stillbirth_mort=False)
            maternal_disability_life = calc_daly_annual(p_mat_morbid * mat_dw[disability], pars_country, start_year=start_year, end_year=end_year)

    for d, disability in enumerate(neo_morb.keys()):
        if neo_dw_lifelong[disability]:
            # Use ghost generating function to track the population of people with comorbidities over time
            p_mat_morbid, p_child_morbid, p_neo_morbid, p_stillbirth_morbid, p_preg_averted_labour, p_preg_averted_education \
                = population_structure(pars_country, np.array([0]), np.array([0]), neo_morb[disability], np.array([0]), np.array([0]), start_year=start_year, end_year=end_year, include_fp_stillbirth_mort=False)
            neonatal_disability_life = calc_daly_annual(p_neo_morbid * neo_dw[disability], pars_country, start_year=start_year, end_year=end_year)

    for d, disability in enumerate(child_morb.keys()):
        if child_dw_lifelong[disability]:
            # Use ghost generating function to track the population of people with comorbidities over time
            p_mat_morbid, p_child_morbid, p_neo_morbid, p_stillbirth_morbid, p_preg_averted_labour, p_preg_averted_education \
                = population_structure(pars_country, np.array([0]), child_morb[disability], np.array([0]), np.array([0]), np.array([0]), start_year=start_year, end_year=end_year, include_fp_stillbirth_mort=False)
            if disability == 'Stunting':
                benefit_adjustment = child_dw[disability] * (pars_country['GDP per capita'][0] / pars_country['Average annual salary'][0])
                child_disability_life = calc_work_benefits(p_child_morbid * benefit_adjustment, pars_country, work_participation=pars_country['Workforce participation'][0], prop_year=1, start_year=start_year, end_year=end_year)
            else:
                child_disability_life = calc_daly_annual(p_child_morbid * child_dw[disability], pars_country, start_year=start_year, end_year=end_year)

    daly = [sum(x) for x in zip(daly_benefit, maternal_disability_life, child_disability_life, neonatal_disability_life)]

    return daly


def calc_daly(pars_country, mat_death, mat_morb, neo_death, neo_morb, child_death, child_morb, stillbirth):
    '''
    This function can be used if the DALYs from years of life lost are all to be attributed to the year that someone dies,
    rather than attributing them to the year that they would otherwise have lived (the calc_daly_annual function, below.
    :param pars_country: Dataframe with parameters for specific country or setting
    :param mat_death: A vector of maternal deaths averted per simulation year
    :param mat_morb: A dictionary of vectors of maternal morbidities (HIV, STI, TB, etc.) averted per simulation year
    :param neo_death: A vector of neonatal deaths averted per simulation year
    :param neo_morb: A dictionary of vectors of neonatal morbidities (HIV, preterm, LBW, etc.) averted per simulation year
    :param child_death: A vector of child under 5 deaths averted per simulation year
    :param child_morb: A dictionary of vectors of child morbidities (HIV, preterm, LBW, etc.) averted per simulation year
    :param stillbirth: A vector of stillbirths averted per simulation year
    :param life_exp: Average life expectancy
    :param avg_age_mat_death: Average age of pregnant women at time of death
    :param discount: The per annum discount rate for DALY impact
    :param stillbirth: Proportion of stillbirth which occur antepartum
    :return: A vector of DALYs averted per simulation year disaggregated by [neonatal YLLs, maternal YLLs, stillbirth YLLs,
             neonatal YLDs, maternal YLDs, total YLLs, total YLDs, total DALYs]
    '''

    # DALY weights for different conditions (proxy values) HIV from LiST assumptions
    mat_dw = {'YLD': 1, 'HIV': 0.33, 'STI': 0.21, 'TB': 0.25, 'General': 0.10}
    neo_dw = {'YLD': 1, 'HIV': 0.221, 'Preterm': 0, 'LBW': 0, 'General': 0.10}
    child_dw = {'YLD': 1, 'Stunting': 0.66, 'Wasting': 0.128 * pars_country['Percent wasting severe'][0], 'General': 0.10}
    mat_dw_lifelong = {'YLD': False, 'HIV': True, 'STI': False, 'TB': True,
                       'General': False}  # Flags for whether these conditions are lifelong
    neo_dw_lifelong = {'YLD': False, 'HIV': True, 'Preterm': True, 'LBW': True, 'General': False}
    child_dw_lifelong = {'YLD': False, 'Stunting': True, 'Wasting': False}

    years = list(range(1, len(mat_death)+1)) # time vector for how many years of health impacts / data are entered

    daly = []
    # Calculate discounted years of life lost from a single maternal, newborn or child death
    maternal_discount = (sum([1 / ((1 + pars_country['Discounting'][0]) ** t) for t in list(range(0, int(pars_country['Expectation of life for women aged 25-29 years'][0] - pars_country['Average age of pregnancy'][0])))]))
    neonatal_discount = (sum([1 / ((1 + pars_country['Discounting'][0]) ** t) for t in list(range(0, int(pars_country['Expectation of life for women aged 25-29 years'][0])))]))
    child_discount = (sum([1 / ((1 + pars_country['Discounting'][0]) ** t) for t in list(range(0, int(pars_country['Expectation of life for women aged 25-29 years'][0])))]))

    for year in years:
        # Calculate total years of life lost attributable to deaths in a given year.
        # Additional discounting is to adjust for the deaths not occurring in year zero
        neonatal_death_YLL = neo_death[year - 1] * neonatal_discount * (1 / ((1 + pars_country['Discounting'][0]) ** (year+2))) # 2020 is year 0
        children_death_YLL = child_death[year - 1] * child_discount * (1 / ((1 + pars_country['Discounting'][0]) ** (year+2)))
        maternal_death_YLL = mat_death[year - 1] * maternal_discount * (1 / ((1 + pars_country['Discounting'][0]) ** (year+2)))
        stillbirth_YLL = stillbirth[year - 1] * pars_country['Intrapartum stillbirth proportion'][0] * neonatal_discount * (1 / ((1 + pars_country['Discounting'][0]) ** (year+2)))  # using proportion intrapartum
        total_YLL = maternal_death_YLL + neonatal_death_YLL + children_death_YLL + stillbirth_YLL # Total YLL from deaths occurring in year

        # Calculate YLD in year. This section will be skipped if no disability data is entered
        maternal_disability = 0
        neonatal_disability = 0
        child_disability = 0
        if bool(mat_morb): # Check if maternal morbidity values are entered. mat_morb is a dictionary of vectors for difference morbidities
            for d, disability in enumerate(mat_morb.keys()):
                if mat_dw_lifelong[disability]:
                    maternal_disability += mat_morb[disability][year - 1] * maternal_discount * mat_dw[disability] * (1 / ((1 + pars_country['Discounting'][0]) ** (year+2)))
                else:
                    maternal_disability += mat_morb[disability][year - 1] * mat_dw[disability] * (1 / ((1 + pars_country['Discounting'][0]) ** (year+2)))
        if bool(neo_morb): # Check if neonatal morbidity values are entered
            for d, disability in enumerate(neo_morb.keys()):
                if neo_dw_lifelong[disability]:
                    neonatal_disability += neo_morb[disability][year - 1] * neonatal_discount * neo_dw[disability] * (1 / ((1 + pars_country['Discounting'][0]) ** (year+2)))
                else:
                    neonatal_disability += neo_morb[disability][year - 1] * neo_dw[disability] * (1 / ((1 + pars_country['Discounting'][0]) ** (year+2)))
        if bool(child_morb): # Check if child morbidity values are entered
            for d, disability in enumerate(child_morb.keys()):
                if child_dw_lifelong[disability]:
                    child_disability += child_morb[disability][year - 1] * child_dw[disability] * (1 / ((1 + pars_country['Discounting'][0]) ** (year+2)))
                else:
                    child_disability += child_morb[disability][year - 1] * child_discount * child_dw[disability] * (1 / ((1 + pars_country['Discounting'][0]) ** (year+2)))
        total_YLD = maternal_disability + neonatal_disability + child_disability

        daly_total = total_YLL + total_YLD # add total YLL and YLD, attributed to outcomes in year
        daly.append([neonatal_death_YLL, children_death_YLL, maternal_death_YLL, stillbirth_YLL, neonatal_disability, child_disability, maternal_disability,
                     total_YLL, total_YLD, daly_total])

    return daly