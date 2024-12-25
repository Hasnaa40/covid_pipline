import sqlite3

def create_sqlite_db():
    # Connect to SQLite database (it will create the database file if it doesn't exist)
    conn = sqlite3.connect('covid_vaccine.db')
    cursor = conn.cursor()

    # Create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS covid_vaccine_data (
            country TEXT,
            total_cases INTEGER,
            total_deaths INTEGER,
            infection_rate REAL,
            total_vaccinations INTEGER,
            vaccination_rate REAL,
            net_infection_rate REAL
        )
    ''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    print("Database and table created successfully.")

# Call the function to create the database and table
create_sqlite_db()
