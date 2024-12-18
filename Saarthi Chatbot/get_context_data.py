from neo4j import GraphDatabase
import requests
from neo4j.exceptions import CypherSyntaxError
import re
import os
import json

def connect_to_graph_db(uri, auth):
    # print("--------- connect_to_graph_db --------------")
    driver = GraphDatabase.driver(uri, auth=auth)
    verify_connection(driver)
    return driver

def verify_connection(driver):
    # print("--------- verify_connection --------------")
    with driver.session() as session:
        try:
            session.run("RETURN 1")  # Simple query to check connection
            print("Connection to the database was successful.")
        except Exception as e:
            print(f"Error connecting to the database: {e}")

def close_graph_db(driver):
    driver.close()


def query_database(driver, cypher_query, params={}):
    # print("--------- query_database --------------")

    # Check for any destructive keywords
    destructive_keywords = ["DELETE", "DETACH DELETE", "DROP", "CREATE", "SET", "MERGE", "REMOVE"]
    if any(re.search(rf"\b{keyword}\b", cypher_query, re.IGNORECASE) for keyword in destructive_keywords):
        raise ValueError("Query contains schema-altering or destructive operations and is not allowed.")

    with driver.session() as session:
        result = session.run(cypher_query, params)
        return [dict(record) for record in result]


def run_direct_query(uri, auth, query, params):
    try:
        driver = connect_to_graph_db(uri, auth)
        result = query_database(driver, query, params)
        return result
    except Exception as e:
        print(f"Error while querying the database: {e}")
        return []

# Get Crime details of the given Zipcode
def get_crime_context(uri, auth, zipcode):
    query = """
    MATCH (:Zipcode {zipcode: $zipcode})-[:has_Crime]->(c:Crime)
    RETURN 
        c.crime_detail AS crimeDetail, 
        c.crime_area_stat AS areaStats, 
        c.crime_national_average AS nationalAverage
    """
    params = {"zipcode": zipcode}
    crime_context = run_direct_query(uri, auth, query, params)
    
    for crime in crime_context:
        crime['areaStats'] = json.loads(crime['areaStats'])
        crime['nationalAverage'] = json.loads(crime['nationalAverage'])
    
    return crime_context
    
# Get Top 5 Restaurants
def get_restaurant_context(uri, auth, zipcode):
    query = " MATCH (:Zipcode {zipcode: $zipcode})-[:has_Restaurants]->(r:Restaurant) RETURN r.restaurant_name AS restaurantName, r.restaurant_rating AS rating, r.restaurant_cuisine AS cuisine, r.restaurant_price AS price, r.restaurant_address AS address, r.restaurant_url AS url ORDER BY r.restaurant_rating DESC LIMIT 5 "
    params = {"zipcode": zipcode}
    restaurant_context = run_direct_query(uri, auth, query, params)
    return restaurant_context
    
# Get Top 5 Restaurants with given Cuisine
def get_restaurant_cuisine_context(uri, auth, zipcode, cuisine= None):
    query = " MATCH (:Zipcode {zipcode: $zipcode})-[:has_Restaurants]->(r:Restaurant) WHERE r.restaurant_cuisine CONTAINS $cuisine RETURN r.restaurant_name AS restaurantName, r.restaurant_rating AS rating, r.restaurant_cuisine AS cuisine, r.restaurant_price AS price, r.restaurant_address AS address, r.restaurant_url AS url ORDER BY r.restaurant_rating DESC LIMIT 5 "
    params = {"zipcode": zipcode, "cuisine": cuisine}
    restaurant_context = run_direct_query(uri, auth, query, params)
    return restaurant_context
    

# Get Top 5 Parks
def get_park_context(uri, auth, zipcode):
    query = " MATCH (:Zipcode {zipcode: $zipcode})-[:has_Parks]->(p:Park) RETURN p.openspace_name AS parkName, p.openspace_type AS type, p.openspace_acreage AS acreage, p.openspace_address AS address LIMIT 5 "
    params = {"zipcode": zipcode}
    park_context = run_direct_query(uri, auth, query, params)
    return park_context
    

# Get Top 5 
def get_demographics_context(uri, auth,zipcode):
    "no code yet"


if __name__ == "__main__":
   
    openai_key = os.getenv("OPENAI_API_KEY")
    neo4j_URI = os.getenv("NEO4J_URI")
    neo4j_AUTH = (os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))

    zipcode = "02215"

    # Get top 5 restaurants
    restaurants = get_restaurant_context(neo4j_URI, neo4j_AUTH, zipcode)
    print(f"restaurants near {zipcode}:")
    print(json.dumps(restaurants, indent=2))
    print("###################################")

    cuisine = "Indian"
    # Get top 5 restaurants with a specific cuisine
    restaurants_with_cuisine = get_restaurant_cuisine_context(neo4j_URI, neo4j_AUTH, zipcode, cuisine)
    print(f"restaurants with cuisine near {zipcode}:")
    print(json.dumps(restaurants_with_cuisine, indent=2))
    print("###################################")

    # Get top 5 parks
    parks_data = get_park_context(neo4j_URI, neo4j_AUTH, zipcode)
    print(f"Parks near {zipcode}:")
    print(json.dumps(parks_data, indent=2))
    print("###################################")

    # Get top 5 parks
    crime_data = get_crime_context(neo4j_URI, neo4j_AUTH, zipcode)
    print("Crime Data:")
    print(json.dumps(crime_data, indent=2))



