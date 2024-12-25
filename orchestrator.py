import logging
from extract import fetch_covid_data, fetch_vaccination_data, fetch_population_data
from transform import transform_covid_data, transform_vaccine_data, final_transformation
from load import load_data_to_sqlite

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def orchestrate_pipeline(countries_list):
    try:
        # Step 1: Extract Data
        logger.info("Starting data extraction...")
        covid_data = fetch_covid_data(countries_list)
        logger.info(f"COVID data shape: {covid_data.shape}")
        logger.info(f"COVID data sample: {covid_data.head()}")
        
        vaccine_data = fetch_vaccination_data(countries_list)
        logger.info(f"Vaccine data shape: {vaccine_data.shape}")
        logger.info(f"Vaccine data sample: {vaccine_data.head()}")
        
        population_data = fetch_population_data(countries_list)
        logger.info(f"Population data shape: {population_data.shape}")
        logger.info(f"Population data sample: {population_data.head()}")

        logger.info("Data extraction completed.")

        # Step 2: Transform Data
        logger.info("Starting data transformation...")
        covid_data_transformed = transform_covid_data(covid_data, population_data)
        logger.info(f"Transformed COVID data shape: {covid_data_transformed.shape}")
        
        vaccine_data_transformed = transform_vaccine_data(vaccine_data, population_data)
        logger.info(f"Transformed vaccine data shape: {vaccine_data_transformed.shape}")
        
        final_data = final_transformation(covid_data_transformed, vaccine_data_transformed)
        logger.info(f"Final data shape: {final_data.shape}")
        logger.info(f"Final data sample: {final_data.head()}")

        logger.info("Data transformation completed.")

        # Step 3: Load Data to SQLite
        logger.info("Starting data load...")
        if not final_data.empty:
            load_data_to_sqlite(final_data, db_file='covid_vaccine.db', table_name='covid_vaccine_data')
            logger.info("Data load completed.")
        else:
            logger.error("No data to load into database - final dataset is empty")

    except Exception as e:
        logger.error(f"An error occurred during the pipeline: {e}")
        raise  # Re-raise the exception to see the full traceback

if __name__ == "__main__":
    # List of countries (example)
    countries_list = [
        "USA",
        "GBR",  # United Kingdom
        "DEU",  # Germany
        "FRA",  # France
        "ITA"   # Italy
    ]

    # Run the pipeline
    orchestrate_pipeline(countries_list)
