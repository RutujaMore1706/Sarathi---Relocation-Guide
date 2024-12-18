import os
from dotenv import load_dotenv
import pandas as pd
import snowflake.connector

# Load environment variables from .env file
load_dotenv()

# Connection parameters
account = os.getenv('account')
user = os.getenv('user')
password = os.getenv('password')
warehouse = os.getenv('warehouse')
database = os.getenv('database')
schema = os.getenv('schema')

# Establish connection to Snowflake
conn = snowflake.connector.connect(
    account=account,
    user=user,
    password=password,
    warehouse=warehouse,
    database=database,
    schema=schema
)

# SQL query to select data from the table
query = "SELECT * FROM OPEN_SPACE_GROUND"

# Use pandas to read the data into a DataFrame
df = pd.read_sql(query, conn)

# Show the first 5 rows of the DataFrame
print(df.head())

# Close the connection
conn.close()



import os
from graph_structure_entity_linking import GraphDB

URI = "neo4j+s://6f4de360.databases.neo4j.io:7687"  
AUTH = ("neo4j", "yVsGWUmODVg0hAFAioEcWSLdzgFpQAO7k6kD2mjpOoE")

class Manager(GraphDB):
    def __init__(self, uri, auth):
        super().__init__(uri, auth)

    def get_existing_zipcodes(self):
        with self.driver.session() as session:
            result = session.run("MATCH (z:Zipcode) RETURN z.zipcode AS zipcode")
            return [record["zipcode"] for record in result]

def insert_zipcodes(zipcodes):
    manager = Manager(URI, AUTH) 
    existing_zipcodes = manager.get_existing_zipcodes()  # Get existing zip codes
    
    for zipcode in zipcodes:
        if zipcode not in existing_zipcodes:  # Check if the zipcode is in the list of existing zip codes
            manager.create_zipcode(zipcode)  
            print(f"Inserted zipcode: {zipcode}")
        else:
            print(f"Zipcode {zipcode} already exists. Skipping insertion.")
    
    manager.close()  # Close the connection

if __name__ == "__main__":
    new_zipcodes = ["02215", "02116", "02118", "02134"]
    insert_zipcodes(new_zipcodes)

