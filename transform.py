import pandas as pd

def transform_covid_data(covid_data, population_data):
    """
    Transforms and merges COVID-19 and population data into a single DataFrame.
    """
    # Merge the COVID data with the population data on the 'country' column
    covid_data = covid_data.merge(population_data, on="country", how="inner")

    # Calculate additional columns such as infection rate
    covid_data['infection_rate'] = (covid_data['total_confirmed'] / covid_data['population']) * 100
    
    # Filter out countries with missing COVID data or population
    covid_data = covid_data.dropna(subset=['total_confirmed', 'total_deaths', 'population'])

    # Rename columns for clarity
    covid_data = covid_data.rename(columns={
        'total_confirmed': 'total_cases',
        'total_deaths': 'total_deaths',
        'population': 'population',
        'country': 'country'
    })

    print("COVID data transformed and merged successfully.")
    return covid_data

def transform_vaccine_data(vaccine_data, population_data):
    """
    Transforms and merges vaccine data with population data.
    """
    # Merge the vaccination data with the population data on the 'country' column
    vaccine_data = vaccine_data.merge(population_data, on="country", how="inner")
    
    # Calculate vaccination rate
    vaccine_data['vaccination_rate'] = (vaccine_data['total_vaccinations'] / vaccine_data['population']) * 100
    
    # Filter out countries with missing vaccination data or population
    vaccine_data = vaccine_data.dropna(subset=['total_vaccinations', 'population'])

    print("Vaccination data transformed and merged successfully.")
    return vaccine_data

def final_transformation(covid_data, vaccine_data):
    """
    Merges the transformed COVID data and vaccine data into a final dataset.
    """
    # Merge the two datasets on the 'country' column
    final_data = pd.merge(covid_data, vaccine_data, on="country", how="inner")
    
    # Calculate the net infection rate (COVID-19 cases minus vaccinated)
    final_data['net_infection_rate'] = final_data['infection_rate'] - final_data['vaccination_rate']
    
    # Filter and sort data based on net infection rate for better insights
    final_data = final_data[['country', 'total_cases', 'total_deaths', 'infection_rate', 'total_vaccinations', 'vaccination_rate', 'net_infection_rate']]
    final_data = final_data.sort_values(by='net_infection_rate', ascending=False)

    print("Final transformation completed.")
    return final_data
