import pandas as pd

def save_to_csv(data, file_name):
    """
    Saves the transformed data to a CSV file.
    """
    data.to_csv(file_name, index=False)
    print(f"Data successfully saved to {file_name}")

def save_to_database(data, db_connection_string, table_name):
    """
    Saves the transformed data to a database (e.g., SQLite, PostgreSQL, MySQL).
    Assumes the necessary database driver is installed.
    """
    # Create a database connection
    from sqlalchemy import create_engine
    engine = create_engine(db_connection_string)

    # Save the data to the specified table in the database
    data.to_sql(table_name, engine, if_exists='replace', index=False)
    print(f"Data successfully saved to {table_name} in the database.")

def load_data(file_name="final_data.csv", db_connection_string=None, table_name="covid_vaccine_data"):
    """
    Loads the transformed data into a file or a database.
    """
    # Save the final data to a CSV file
    save_to_csv(data, file_name)

    # Optionally, if a database connection string is provided, save the data to the database
    if db_connection_string:
        save_to_database(data, db_connection_string, table_name)

import sqlite3
import pandas as pd

def save_to_sqlite(data, db_file='covid_vaccine.db', table_name='covid_vaccine_data'):
    """
    Saves the transformed data to an SQLite database.
    """
    # Connect to SQLite database (it will create the file if it doesn't exist)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Save data to the specified table in SQLite
    data.to_sql(table_name, conn, if_exists='replace', index=False)
    print(f"Data successfully saved to {table_name} in SQLite database.")

    # Commit changes and close the connection
    conn.commit()
    conn.close()

def load_data_to_sqlite(data, db_file='covid_vaccine.db', table_name='covid_vaccine_data'):
    """
    Loads the transformed data into SQLite database.
    """
    save_to_sqlite(data, db_file, table_name)
