import numpy as np

def population_structure(pars_country, mat_death, child_death, neo_death, stillbirth,
                                                             preg_averted, start_year=2022, end_year=2030, include_fp_stillbirth_mort=False):
    '''
    :param pars_country: Dataframe with parameters for specific country or setting
    :param mat_death:
    :param neo_death:
    :param child_death:
    :param stillbirth:
    :param preg_averted:
    :param start_year: First year of projected benefits
    :param end_year: Final year of projected benefits
    :return:
    '''

    years = list(range(0, end_year - start_year + 1))

    # Initialise matrix of outcome for future workforce that has received additional education
    bg_mort = np.zeros(66)
    bg_mort[0] = pars_country['All cause mortality <1 year'][0]
    bg_mort[1:5] = pars_country['All cause mortality 1-4 year'][0]
    bg_mort[5:10] = pars_country['All cause mortality 5-9 year'][0]
    bg_mort[10:15] = pars_country['All cause mortality 10-14 year'][0]
    bg_mort[15:20] = pars_country['All cause mortality 15-19 year'][0]
    bg_mort[20:25] = pars_country['All cause mortality 20-24 year'][0]
    bg_mort[25:30] = pars_country['All cause mortality 25-29 year'][0]
    bg_mort[30:35] = pars_country['All cause mortality 30-34 year'][0]
    bg_mort[35:40] = pars_country['All cause mortality 35-39 year'][0]
    bg_mort[40:45] = pars_country['All cause mortality 40-44 year'][0]
    bg_mort[45:50] = pars_country['All cause mortality 45-49 year'][0]
    bg_mort[50:55] = pars_country['All cause mortality 50-54 year'][0]
    bg_mort[55:60] = pars_country['All cause mortality 55-59 year'][0]
    bg_mort[60:65] = pars_country['All cause mortality 60-64 year'][0]
    bg_mort[65] = pars_country['All cause mortality 65+ yo'][0]

    '''Maternal mortality averted'''
    # Create array for each age bins up to 66 for each year, and initialize with maternal deaths averted in year zero
    population_mat_death = np.zeros((len(years), 66))
    population_mat_death[0,15:20] = pars_country['Proportion of PW 15-19 yo'][0] * mat_death[0] * 1/5
    population_mat_death[0,20:25] = pars_country['Proportion of PW 20-24 yo'][0] * mat_death[0] * 1/5
    population_mat_death[0, 25:30] = pars_country['Proportion of PW 25-29 yo'][0] * mat_death[0] * 1/5
    population_mat_death[0, 30:35] = pars_country['Proportion of PW 30-34 yo'][0] * mat_death[0] * 1/5
    population_mat_death[0, 35:40] = pars_country['Proportion of PW 35-39 yo'][0] * mat_death[0] * 1/5
    population_mat_death[0, 40:45] = pars_country['Proportion of PW 40-44 yo'][0] * mat_death[0] * 1/5
    population_mat_death[0, 45:50] = pars_country['Proportion of PW 45-49 yo'][0] * mat_death[0] * 1/5

    for year in years[1:]:
        for i in range(1, 66):
            # Age the population, and account for all-cause mortality
            population_mat_death[year, i] = population_mat_death[year - 1, i - 1] - bg_mort[i-1] * population_mat_death[year - 1, i - 1]

        if year < len(mat_death):
            # Add new deaths averted to the population model
            population_mat_death[year, 15:20] += pars_country['Proportion of PW 15-19 yo'][0] * mat_death[year] * 1 / 5
            population_mat_death[year, 20:25] += pars_country['Proportion of PW 20-24 yo'][0] * mat_death[year] * 1 / 5
            population_mat_death[year, 25:30] += pars_country['Proportion of PW 25-29 yo'][0] * mat_death[year] * 1 / 5
            population_mat_death[year, 30:35] += pars_country['Proportion of PW 30-34 yo'][0] * mat_death[year] * 1 / 5
            population_mat_death[year, 35:40] += pars_country['Proportion of PW 35-39 yo'][0] * mat_death[year] * 1 / 5
            population_mat_death[year, 40:45] += pars_country['Proportion of PW 40-44 yo'][0] * mat_death[year] * 1 / 5
            population_mat_death[year, 45:50] += pars_country['Proportion of PW 45-49 yo'][0] * mat_death[year] * 1 / 5

    '''Child'''
    # Create array for each age bins up to 66 for each year, and initialize with child deaths averted in year zero
    population_child_death = np.zeros((len(years), 66))
    population_child_death[0, 1:5] = child_death[0] * 1 / 4

    for year in years[1:]:
        for i in range(1, 66):
            # Age the population, and account for all-cause mortality
            population_child_death[year, i] = population_child_death[year - 1, i - 1] - bg_mort[i - 1] * population_child_death[year - 1, i - 1]
        if year < len(child_death):
            # Add new deaths averted to the population model
            population_child_death[year, 1:5] += child_death[year] * 1 / 4

    '''Neonatal'''
    # Create array for each age bins up to 66 for each year, and initialize with neonatal deaths averted in year zero
    population_neo_death = np.zeros((len(years), 66))
    population_neo_death[0, 0] = neo_death[0]

    for year in years[1:]:
        for i in range(1, 66):
            # Age the population, and account for all-cause mortality
            population_neo_death[year, i] = population_neo_death[year - 1, i - 1] - bg_mort[i - 1] * population_neo_death[year - 1, i - 1]
        if year < len(neo_death):
            # Add new deaths averted to the population model
            population_neo_death[year, 0] += neo_death[year] # Update with current years input
            if include_fp_stillbirth_mort: # INCLUDE THESE TO COUNT STILLBIRTHS + NEONATAL DEATHS AVERTED FROM UNWANTED PREGNANCIES AVERTED
                population_neo_death[year, 0] += preg_averted[year] * (pars_country['Neonatal mortality rate'][0] / 1000)


    '''Stillbirth'''
    # Create array for each age bins up to 66 for each year, and initialize with stillbirths averted in year zero
    population_stillbirth = np.zeros((len(years), 66))
    population_stillbirth[0, 0] = stillbirth[0] * pars_country['Intrapartum stillbirth proportion'][0]

    for year in years[1:]:
        for i in range(1, 66):
            # Age the population, and account for all-cause mortality
            population_stillbirth[year, i] = population_stillbirth[year - 1, i - 1] - bg_mort[i - 1] * population_stillbirth[year - 1, i - 1]
        if year < len(stillbirth):
            # Add new deaths averted to the population model
            population_stillbirth[year, 0] += stillbirth[year] * pars_country['Intrapartum stillbirth proportion'][0]  # Update with current years input
            if include_fp_stillbirth_mort: # INCLUDE THESE TO COUNT STILLBIRTHS + NEONATAL DEATHS AVERTED FROM UNWANTED PREGNANCIES AVERTED
                population_stillbirth[year, 0] += preg_averted[year] * (pars_country['Stillbirth rate'][0] / 1000) \
                                                 * pars_country['Intrapartum stillbirth proportion'][0]

    '''Pregnancy averted for labour calculations'''
    # Create array for each age bins up to 66 for each year, and initialize with pregnancies averted in year zero
    population_preg_averted_labour = np.zeros((len(years), 66))
    population_preg_averted_labour[0, 15:20] += pars_country['Proportion of PW 15-19 yo'][0] * preg_averted[0] * 1 / 5
    population_preg_averted_labour[0, 20:25] += pars_country['Proportion of PW 20-24 yo'][0] * preg_averted[0] * 1 / 5
    population_preg_averted_labour[0, 25:30] += pars_country['Proportion of PW 25-29 yo'][0] * preg_averted[0] * 1 / 5
    population_preg_averted_labour[0, 30:35] += pars_country['Proportion of PW 30-34 yo'][0] * preg_averted[0] * 1 / 5
    population_preg_averted_labour[0, 35:40] += pars_country['Proportion of PW 35-39 yo'][0] * preg_averted[0] * 1 / 5
    population_preg_averted_labour[0, 40:45] += pars_country['Proportion of PW 40-44 yo'][0] * preg_averted[0] * 1 / 5
    population_preg_averted_labour[0, 45:50] += pars_country['Proportion of PW 45-49 yo'][0] * preg_averted[0] * 1 / 5
    for year in years[1:]:
        if year < len(preg_averted):
            # Add new pregnancies averted to the population model, no ageing as labour benefits are short term
            population_preg_averted_labour[year, 15:20] += pars_country['Proportion of PW 15-19 yo'][0] * preg_averted[year] * 1 / 5
            population_preg_averted_labour[year, 20:25] += pars_country['Proportion of PW 20-24 yo'][0] * preg_averted[year] * 1 / 5
            population_preg_averted_labour[year, 25:30] += pars_country['Proportion of PW 25-29 yo'][0] * preg_averted[year] * 1 / 5
            population_preg_averted_labour[year, 30:35] += pars_country['Proportion of PW 30-34 yo'][0] * preg_averted[year] * 1 / 5
            population_preg_averted_labour[year, 35:40] += pars_country['Proportion of PW 35-39 yo'][0] * preg_averted[year] * 1 / 5
            population_preg_averted_labour[year, 40:45] += pars_country['Proportion of PW 40-44 yo'][0] * preg_averted[year] * 1 / 5
            population_preg_averted_labour[year, 45:50] += pars_country['Proportion of PW 45-49 yo'][0] * preg_averted[year] * 1 / 5

    '''Pregnancy averted for education calculations'''
    # Create array for each age bins up to 66 for each year, and initialize with adolescent pregnancies averted in year zero
    population_preg_averted_education = np.zeros((len(years), 66))
    population_preg_averted_education[0, 15:18] = pars_country['Proportion of PW 15-19 yo'][0] * preg_averted[0] * 1 / 5

    for year in years[1:]:
        for i in range(1, 66):
            # Age the population who recieve extra education, and account for all-cause mortality
            population_preg_averted_education[year, i] = population_preg_averted_education[year - 1, i - 1] - bg_mort[i - 1] * population_preg_averted_education[year - 1, i - 1]
        if year < len(preg_averted):
            population_preg_averted_education[year, 15:18] += pars_country['Proportion of PW 15-19 yo'][0] * preg_averted[year] * 1 / 5

    return (population_mat_death, population_child_death, population_neo_death, population_stillbirth, population_preg_averted_labour, population_preg_averted_education)


