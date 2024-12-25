import requests
import pandas as pd
countries_list = [
    "USA"]
# Function to fetch COVID-19 data from the JHU CSSE dataset via the disease.sh API
def fetch_covid_data(countries):
    """
    Fetches COVID-19 data from the JHU CSSE dataset via the disease.sh API.
    Returns a cleaned and formatted DataFrame.
    """
    covid_data_list = []
    
    for country in countries:
        # Using disease.sh API which provides historical data
        api_url = f"https://disease.sh/v3/covid-19/countries/{country}"
        response = requests.get(api_url)
        
        if response.status_code == 200:
            data = response.json()
            
            country_data = {
                'country': country,
                'total_confirmed': data.get('cases', 0),
                'total_deaths': data.get('deaths', 0),
                'date': pd.Timestamp.now().strftime('%Y-%m-%d')
            }
            covid_data_list.append(country_data)
            print(f"Successfully fetched COVID data for {country}")
        else:
            print(f"Failed to fetch data for {country}: {response.status_code}")
    
    # Convert list of data into DataFrame
    covid_data = pd.DataFrame(covid_data_list)
    
    print("COVID-19 data fetched and cleaned successfully.")
    return covid_data


def fetch_population_data(countries):
    """
    Fetches population data from the World Bank API.
    Returns a cleaned and formatted DataFrame.
    """
    # World Bank population data API (Indicator: SP.POP.TOTL - Total Population)
    population_url = "http://api.worldbank.org/v2/country/{}/indicator/SP.POP.TOTL?format=json&date=2022"

    # Initialize an empty list to store the population data
    countries_population = []

    # Loop through the list of countries to fetch the population for each
    for country in countries:
        # Construct the URL for each country by using its ISO code
        country_url = population_url.format(country)
        response = requests.get(country_url)

        # Check if the response is valid
        if response.status_code == 200:
            data = response.json()
            if len(data) > 1 and 'value' in data[1][0]:  # Ensure the data exists
                population = data[1][0]['value']
                countries_population.append({'country': country, 'population': population})

    # Convert list to DataFrame
    population_data = pd.DataFrame(countries_population)

    print(f"Population data fetched for {len(population_data)} countries.")
    return population_data

def fetch_vaccination_data(countries):
    """
    Fetches vaccination data from the disease.sh API.
    Returns a cleaned and formatted DataFrame.
    """
    vaccination_data_list = []
    
    for country in countries:
        api_url = f"https://disease.sh/v3/covid-19/vaccine/coverage/countries/{country}?lastdays=1"
        response = requests.get(api_url)
        
        if response.status_code == 200:
            data = response.json()
            timeline = data.get('timeline', {})
            # Get the last date's vaccination data
            last_date = list(timeline.keys())[-1] if timeline else None
            total_vaccinations = timeline[last_date] if last_date else 0
            
            vaccination_data_list.append({
                'country': country,
                'total_vaccinations': total_vaccinations
            })
            print(f"Successfully fetched vaccination data for {country}")
        else:
            print(f"Failed to fetch vaccination data for {country}: {response.status_code}")
    
    # Convert to DataFrame
    vaccination_data = pd.DataFrame(vaccination_data_list)
    
    print("Vaccination data fetched and cleaned successfully.")
    return vaccination_data
