import os
from dotenv import load_dotenv
import pandas as pd
import snowflake.connector
from graph_structure_entity_linking import GraphDB
import googlemaps
import random
import re
from sentence_transformers import SentenceTransformer

# Load environment variables from .env file
load_dotenv()

# Snowflake connection parameters
snowflake_params = {
    'account': os.getenv('account'),
    'user': os.getenv('user'),
    'password': os.getenv('password'),
    'warehouse': os.getenv('warehouse'),
    'database': os.getenv('database'),
    'schema': os.getenv('schema')
}

# Neo4j connection parameters
neo4j_uri = "neo4j+s://6f4de360.databases.neo4j.io:7687"
neo4j_auth = ("neo4j", "yVsGWUmODVg0hAFAioEcWSLdzgFpQAO7k6kD2mjpOoE")

class Manager(GraphDB):
    def __init__(self, uri, auth):
        super().__init__(uri, auth)

    def get_existing_zipcodes(self):
        with self.driver.session() as session:
            result = session.run("MATCH (z:Zipcode) RETURN z.zipcode AS zipcode")
            return [record["zipcode"] for record in result]
        
    def get_existing_parks(self):
        with self.driver.session() as session:
            result = session.run("MATCH (p:Park) RETURN p.openspace_name AS name")
            return [record["name"] for record in result]
    
    def get_existing_subway(self):
        with self.driver.session() as session:
            result = session.run("MATCH (s:Subway) RETURN s.subway_station_name AS name")
            return [record["name"] for record in result]
        
    def get_existing_restaurants(self):
        with self.driver.session() as session:
            result = session.run("MATCH (r:Restaurant) RETURN r.restaurant_id AS id")
            return [record["id"] for record in result]
    
    def get_existing_census(self):
        with self.driver.session() as session:
            result = session.run("MATCH (c:Census) RETURN c.zipcode AS zipcode")
            return [record["zipcode"] for record in result]
        
    def get_existing_groups(self):
        with self.driver.session() as session:
            result = session.run("MATCH (m:MeetupGroup) RETURN m.meetup_group_name AS name")
            return [record["name"] for record in result]

    def get_existing_utilities(self):
        with self.driver.session() as session:
            result = session.run("MATCH (u:Utilities) RETURN u.zipcode AS zipcode")
            return [record["zipcode"] for record in result]
        
    def get_existing_crimes(self):
        with self.driver.session() as session:
            result = session.run("MATCH (c:Crime) RETURN c.zipcode AS zipcode")
            return [record["zipcode"] for record in result]
    
    def get_existing_apartments(self):
        with self.driver.session() as session:
            result = session.run("MATCH (a:Apartment) RETURN a.apt_zpid AS zpid")
            return [record["zpid"] for record in result]
    
    def get_existing_violations(self):
        with self.driver.session() as session:
            result = session.run("MATCH (v:Violation) RETURN v.date AS date, v.address AS address")
            return [{"date": record["date"], "address": record["address"]} for record in result]

    ################################################## Realtionship Restaurant & Park & Subway ####################################################
    def get_walking_time_and_distance(self, lat1, lon1, lat2, lon2):
        """Use Google Maps API to calculate walking time and distance."""
        gmaps = googlemaps.Client(key=os.getenv('maps_api'))
        origin = (lat1, lon1)
        destination = (lat2, lon2)
        try:
            result = gmaps.distance_matrix(origins=origin, destinations=destination, mode='walking')
            # Extract duration and distance
            walking_time = result['rows'][0]['elements'][0]['duration']['text']
            distance = result['rows'][0]['elements'][0]['distance']['text']
            return walking_time, distance
        except Exception as e:
            print(f"Error calculating walking distance: {e}")
            return None, None
    
    '''
    def fetch_existing_relationship_restaurant(self):
        """Fetch all existing HAS_NEARBY_RESTAURANT relationships from the database."""
        query = """
        MATCH (a:Apartment)-[r:HAS_NEARBY_RESTAURANT]->(rest:Restaurant)
        RETURN a.apt_zpid AS apartment_zpid, rest.restaurant_id AS restaurant_id
        """
        result = self.graph.run(query)
        # Convert result to a DataFrame for easy lookups
        return pd.DataFrame(result.data())
    '''
    def fetch_existing_relationship_restaurant(self):
        """Fetch all existing HAS_NEARBY_RESTAURANT relationships from the database."""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (a:Apartment)-[r:has_nearby_restaurant]->(rest:Restaurant)
                RETURN a.apt_zpid AS apartment_zpid, rest.restaurant_id AS restaurant_id
            """)
            records = [{"apartment_zpid": record["apartment_zpid"], "restaurant_id": record["restaurant_id"]} for record in result]
            return pd.DataFrame(records)
    '''
    def fetch_existing_relationship_openspace(self):
        """Fetch all existing HAS_NEARBY_PARK relationships from the database."""
        query = """
        MATCH (a:Apartment)-[r:HAS_NEARBY_PARK]->(p:Park)
        RETURN a.apt_zpid AS apartment_zpid, p.openspace_name AS openspace_name
        """
        result = self.graph.run(query)
        # Convert result to a DataFrame for easy lookups
        return pd.DataFrame(result.data())
    '''
    def fetch_existing_relationship_openspace(self):
        """Fetch all existing HAS_NEARBY_PARK relationships from the database."""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (a:Apartment)-[r:has_nearby_park]->(p:Park)
                RETURN a.apt_zpid AS apartment_zpid, p.openspace_name AS openspace_name
            """)
            
            records = [{"apartment_zpid": record["apartment_zpid"], "openspace_name": record["openspace_name"]} for record in result]
            return pd.DataFrame(records)
    
    def fetch_existing_relationship_subwaystation(self):
        """Fetch all existing HAS_NEARBY_SUBWAY relationships from the database."""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (a:Apartment)-[r:has_nearby_subwaystation]->(s:Subway)
                RETURN a.apt_zpid AS apartment_zpid, s.subway_station_name AS subway_station_name
            """)
            
            records = [{"apartment_zpid": record["apartment_zpid"], "subway_station_name": record["subway_station_name"]} for record in result]
            return pd.DataFrame(records)
    ###############################################################################################################################
        
def insert_zipcodes(zipcodes_df):
    manager = Manager(neo4j_uri, neo4j_auth)
    existing_zipcodes = manager.get_existing_zipcodes()

    for index, row in zipcodes_df.iterrows():
        zipcode  = row['ZIP_CODE']
        if zipcode not in existing_zipcodes:
            manager.create_zipcode(
                zipcode = zipcode,
                neighborhood = row['NEIGHBORHOOD'],
                summary = row['SUMMARY'],
                walk_score = row['WALK_SCORE'],
                transit_score = ['TRANSIT_SCORE']
                )
            print(f"Inserted zipcode: {zipcode}")
        else:
            print(f"Zipcode {zipcode} already exists. Skipping insertion.")

    manager.close()

def insert_parks(parks_df):
    manager = Manager(neo4j_uri, neo4j_auth)
    existing_parks = manager.get_existing_parks()

    for index, row in parks_df.iterrows():
        park_name = row['SITE_NAME']
        if park_name not in existing_parks:  
            manager.create_park(
                name=park_name,
                address=row["ADDRESS"],
                acreage=row['AREA'],
                type_=row['TYPE'],
                zipcode=row['ZIP_CODE']
                )
            print(f"Inserted park: {park_name}")
        else:
            print(f"Park {park_name} already exists. Skipping insertion.")
    manager.close()

def insert_subway(subway_df):
    manager = Manager(neo4j_uri, neo4j_auth)
    existing_subway = manager.get_existing_subway()

    for index, row in subway_df.iterrows():
        subway_station_name = row['STATION']
        if subway_station_name not in existing_subway:  
            manager.create_subway(
                name=subway_station_name,
                line=row["LINE"],
                route=row['ROUTE'],
                zipcode=row['ZIP_CODE'],
                latitude=row['LATITUDE'],
                longitude = row['LONGITUDE']
                )
            print(f"Inserted park: {subway_station_name}")
        else:
            print(f"Park {subway_station_name} already exists. Skipping insertion.")
    manager.close()

def insert_restaurants(restaurants_df):
    manager = Manager(neo4j_uri, neo4j_auth)
    existing_restaurants = manager.get_existing_restaurants()

    for index, row in restaurants_df.iterrows():
        restaurant_id = row['RESTAURANT_ID']
        if restaurant_id not in existing_restaurants:  
            manager.create_restaurant(
                id=restaurant_id,
                name=row['RESTAURANT_NAME'] , 
                cuisine= row['CUISINE'],
                url= row['URL'],
                image_url= row['IMAGE_URL'],
                price=row['PRICE'],
                rating= row['RATING'], 
                latitude= row['LATITUDE'], 
                longitude= row['LONGITUDE'],
                address= row['ADDRESS'],
                zipcode=row['ZIP_CODE']
                )
            print(f"Inserted restaurant: {restaurant_id}")
        else:
            print(f"Restaurant {restaurant_id} already exists. Skipping insertion.")
    manager.close()

def insert_census(census_df):
    manager = Manager(neo4j_uri, neo4j_auth)
    existing_census = manager.get_existing_census()

    for index, row in census_df.iterrows():
        zipcode = row['ZIPCODE']
        if zipcode not in existing_census:  
            manager.create_census(
                zipcode=zipcode,
                population=row['POPULATION'], 
                hispanic_latino=row['HISPANIC_LATINO'],
                white=row['WHITE'],
                black=row['BLACK'],
                american_indian=row['AMERICAN_INDIAN'],
                asian=row['ASIAN'],
                native_hawaiian=row['NATIVE_HAWAIIAN'],
                some_other_race=row['SOME_OTHER_RACE'],
                demographics_education_workforce=row['DEMOGRAPHICS_EDUCATION_WORKFORCE']
                )
            print(f"Inserted census: {zipcode}")
        else:
            print(f"Census {zipcode} already exists. Skipping insertion.")
    manager.close()

def insert_meetup_groups(groups_df):
    manager = Manager(neo4j_uri, neo4j_auth)
    existing_groups = manager.get_existing_groups()

    for index, row in groups_df.iterrows():
        group_name = row['NAME']
        if group_name not in existing_groups:  
            manager.create_meetup_group(
                name=group_name,
                description=row['GROUP_DESCRIPTION'], 
                link=row['GROUP_MEETUP_URL'],
                category=row['CATEGORY'],
                city=row['CITY'],
                zipcode=row['ZIP_CODE'],
                member_count=row['MEMBERCOUNT'],
                past_events=row['PAST_EVENTS'],
                description_vector=row['DESCRIPTION_VECTOR']
                )
            print(f"Inserted group: {group_name}")
        else:
            print(f"{group_name} already exists. Skipping insertion.")
    manager.close()

def insert_utilities(utilities_df):
    manager = Manager(neo4j_uri, neo4j_auth)
    existing_zipcode = manager.get_existing_utilities()

    for index, row in utilities_df.iterrows():
        zipcode = row['ZIP_CODE']
        if zipcode not in existing_zipcode:  
            manager.create_utilities(
                zipcode=zipcode,
                electric=row['ELECTRICITY'],
                natural_gas=row['GAS'],
                steam=row['HEAT'],
                water=row['WATER'], 
                total_cost=row['TOTALCOST'],
                )
            print(f"Inserted utilities: {zipcode}")
        else:
            print(f"utilities {zipcode} already exists. Skipping insertion.")
    manager.close()

def insert_crimes(crimes_df):
    manager = Manager(neo4j_uri, neo4j_auth)
    existing_crimes = manager.get_existing_crimes()

    for index, row in crimes_df.iterrows():
        zipcode = row['ZIP_CODE']
        if zipcode not in existing_crimes:  
            manager.create_crime(
                zipcode=zipcode,
                detail=row['DETAIL'], 
                area_stat=row['AREASTATS'],
                national_average = row['NATIONALAVERAGE']
                )
            print(f"Inserted Crime Data: {zipcode}")
        else:
            print(f"Crime Data for {zipcode} already exists. Skipping insertion.")
    manager.close()

def insert_apartments(apartments_df):
    manager = Manager(neo4j_uri, neo4j_auth)
    existing_apartment = manager.get_existing_apartments()

    for index, row in apartments_df.iterrows():
        zpid = row['APT_ZPID']
        if zpid not in existing_apartment:  
            manager.create_apartment(
                zpid=row['APT_ZPID'] + '--'+str(row['APT_UNIT_NUMBER']),
                address=row['APT_ADDRESS'],  
                bedroom_count=row['APT_BEDROOM_COUNT'],  
                bathroom_count=row['APT_BATHROOM_COUNT'], 
                rent=row['APT_RENT'],  
                living_area=row['APT_LIVING_AREA'],  
                transit_score=random.randrange(80,100,5), 
                latitude=row['APT_LATITUDE'], 
                longitude=row['APT_LONGITUDE'], 
                url=row['APT_URL'],  
                image_url=row['APT_IMAGE_URL'], 
                zipcode=row['APT_ZIP_CODE'],
                building_name=row['APT_BUILDING_NAME'],
                lot_id=row['APT_LOT_ID'],
                property_type=row['APT_PROPERTY_TYPE'],
                unit= row['APT_UNIT_NUMBER']
                )
            print(f"Inserted apartment: {zpid}")
        else:
            print(f"Apartment {zpid} already exists. Skipping insertion.")
    manager.close()

###################################################### INSERT NEARBY RESTAURNATS & Openspace & SUBWAY ############################################################
def parse_walking_time(walking_time):
    """
    Parse the walking time string and convert it into minutes.
    Handles cases like "1 hour 17 mins" or "21 mins".
    """
    total_minutes = 0
    
    # Check if 'hour' is present
    hours_match = re.search(r'(\d+)\s*hour', walking_time)
    if hours_match:
        total_minutes += int(hours_match.group(1)) * 60  
    
    # Check if 'min' is present 
    minutes_match = re.search(r'(\d+)\s*min', walking_time)
    if minutes_match:
        total_minutes += int(minutes_match.group(1))  

    return total_minutes


def create_nearby_restaurant_relationship(apartments_df, restaurants_df):
        manager = Manager(neo4j_uri, neo4j_auth)
        existing_relationships_df = manager.fetch_existing_relationship_restaurant()
        """Iterate over apartments and restaurants, and create relationships if they meet the criteria."""
        for _, apartment in apartments_df.iterrows():
            for _, restaurant in restaurants_df.iterrows():
                # Check if the relationship already exists
                if not existing_relationships_df.empty:
                    exists = existing_relationships_df[
                        (existing_relationships_df['apartment_zpid'] == apartment['APT_ZPID']) &
                        (existing_relationships_df['restaurant_id'] == restaurant['RESTAURANT_ID'])
                    ]
                    if not exists.empty:
                        print(f"Relationship between apartment {apartment['APT_ZPID']} and restaurant {restaurant['RESTAURANT_NAME']} already exists.")
                        continue

                # Calculate walking time and distance
                walking_time, distance = manager.get_walking_time_and_distance(
                    apartment['APT_LATITUDE'], apartment['APT_LONGITUDE'],
                    restaurant['LATITUDE'], restaurant['LONGITUDE']
                )
                print(f" *************** Orignal Walking Time = {walking_time}")
                
                if walking_time:
                    time_in_minutes = parse_walking_time(walking_time)
                    print(f" *************** New Walking Time = {time_in_minutes}")
                    if time_in_minutes <= 10:
                        # Insert relationship only if walking time is within 10 minutes
                        print(f"Inserting nearby relationship: {apartment['APT_ZPID']} -> {restaurant['RESTAURANT_NAME']}")
                        manager.create_nearby_restaurant(
                            apartment_zpid=apartment['APT_ZPID'],
                            restaurant_id=restaurant['RESTAURANT_ID'],
                            walking_time=walking_time,
                            distance=distance
                        )
                    else:
                        print(f"Restaurant {restaurant['RESTAURANT_NAME']} is more than 10 minutes away from apartment {apartment['APT_ZPID']}.")
                else:
                    print(f"Could not calculate walking time for apartment {apartment['APT_ZPID']} and restaurant {restaurant['RESTAURANT_NAME']}.")

def create_nearby_park_relationship(apartments_df, parks_df):
        manager = Manager(neo4j_uri, neo4j_auth)
        existing_relationships_df = manager.fetch_existing_relationship_openspace()
        """Iterate over apartments and parks, and create relationships if they meet the criteria."""
        for _, apartment in apartments_df.iterrows():
            for _, park in parks_df.iterrows():
                # Check if the relationship already exists in the existing_relationships_df
                if not existing_relationships_df.empty:
                    exists = existing_relationships_df[
                        (existing_relationships_df['apartment_zpid'] == apartment['APT_ZPID']) &
                        (existing_relationships_df['openspace_name'] == park['SITE_NAME'])
                    ]
                    if not exists.empty:
                        print(f"Relationship between apartment {apartment['APT_ZPID']} and park {park['SITE_NAME']} already exists.")
                        continue

                # Calculate walking time and distance
                walking_time, distance = manager.get_walking_time_and_distance(
                    apartment['APT_LATITUDE'], apartment['APT_LONGITUDE'],
                    park['LATITUDE'], park['LONGITUDE']
                )

                if walking_time:
                    time_in_minutes = parse_walking_time(walking_time)
                    if time_in_minutes <= 10:
                        # Insert relationship only if walking time is within 10 minutes
                        print(f"Inserting nearby relationship: {apartment['APT_ZPID']} -> {park['SITE_NAME']}")
                        manager.create_nearby_park(
                            apartment_zpid=apartment['APT_ZPID'],
                            park_name=park['SITE_NAME'],
                            walking_time=walking_time,
                            distance=distance
                        )
                    else:
                        print(f"Park {park['SITE_NAME']} is more than 10 minutes away from apartment {apartment['APT_ZPID']}.")
                else:
                    print(f"Could not calculate walking time for apartment {apartment['APT_ZPID']} and park {park['SITE_NAME']}.")




def create_nearby_subway_relationship(apartments_df, subway_df):
        manager = Manager(neo4j_uri, neo4j_auth)
        existing_relationships_df = manager.fetch_existing_relationship_subwaystation()
        """Iterate over apartments and subway, and create relationships if they meet the criteria."""
        for _, apartment in apartments_df.iterrows():
            for _, subway in subway_df.iterrows():
                # Check if the relationship already exists in the existing_relationships_df
                if not existing_relationships_df.empty:
                    exists = existing_relationships_df[
                        (existing_relationships_df['apartment_zpid'] == apartment['APT_ZPID']) &
                        (existing_relationships_df['subway_station_name'] == subway['STATION'])
                    ]
                    if not exists.empty:
                        print(f"Relationship between apartment {apartment['APT_ZPID']} and subway {subway['STATION']} already exists.")
                        continue

                # Calculate walking time and distance
                walking_time, distance = manager.get_walking_time_and_distance(
                    apartment['APT_LATITUDE'], apartment['APT_LONGITUDE'],
                    subway['LATITUDE'], subway['LONGITUDE']
                )

                if walking_time:
                    time_in_minutes = parse_walking_time(walking_time)
                    if time_in_minutes <= 15:
                        # Insert relationship only if walking time is within 10 minutes
                        print(f"Inserting nearby relationship: {apartment['APT_ZPID']} -> {subway['STATION']}")
                        manager.create_nearby_subwaystation(
                            apartment_zpid=apartment['APT_ZPID'],
                            subway_station_name=subway['STATION'],
                            walking_time=walking_time,
                            distance=distance
                        )
                    else:
                        print(f"Subway {subway['STATION']} is more than 10 minutes away from apartment {apartment['APT_ZPID']}.")
                else:
                    print(f"Could not calculate walking time for apartment {apartment['APT_ZPID']} and park {subway['STATION']}.")

# Load Sentence Transformers
model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embeddings(row):
    combined_text = f"{row['NAME']} {row['GROUP_DESCRIPTION']} {row['CATEGORY']}"
    return model.encode(combined_text)

############################################################################################################################################
def main():
    conn = snowflake.connector.connect(**snowflake_params)

    try:
        # Insert Zip
        #new_zipcodes = ["02215", "02116", "02118", "02134"]
        data_neighborhood = {
        "ZIP_CODE": ["02215", "02216", "02118", "02116"],
        "NEIGHBORHOOD": ["Fenway", "South Boston", "South End", "Back Bay"],
        "SUMMARY": [
        """ Fenway is a vibrant Boston neighborhood that seamlessly blends historic charm with modern urban living. At its heart stands the iconic Fenway Park, home to the Boston Red Sox since 1912, which continues to be a major community focal point. The area offers a diverse mix of housing options, from vintage brownstone condos to luxurious high-rise apartments, catering to various preferences and budgets.
Fenway's culinary scene is a highlight, featuring an eclectic array of international cuisines along Boylston Street and Peterborough Street's restaurant row. The neighborhood is also home to convenient shopping options, including the Red Sox Team Store and major retailers like Target.
Nature enthusiasts appreciate the Back Bay Fens, a sprawling green space that's part of Boston's Emerald Necklace. This park offers community gardens, the beautiful Kelleher Rose Garden, and various recreational facilities. Beyond baseball, Fenway hosts numerous events throughout the year, including concerts, festivals, and seasonal gatherings at The Station on Boylston Street.
The area boasts excellent public transportation options, with multiple T stations and bus stops, making it ideal for commuters working in nearby medical institutions or other parts of Boston. For families, Fenway offers access to Boston Public Schools, including the well-regarded Fenway High School.
With its rich history, diverse amenities, and constant development, Fenway continues to be an attractive neighborhood for both residents and visitors alike.""",
        """ South Boston, affectionately known as "Southie," is a vibrant neighborhood that seamlessly blends its rich Irish heritage with modern urban living. Located just 3 miles from downtown Boston, it offers residents stunning waterfront views and easy access to the city center. The area has undergone significant gentrification, becoming a trendy urban locale while maintaining its strong sense of community. Southie's booming real estate market features a mix of historic row houses, converted single-family homes, modern condos, and high-end waterfront properties, with prices ranging from $550,000 to $3 million for luxury condos. The neighborhood keeps residents entertained with numerous beaches, parks, cultural attractions, and a thriving dining and nightlife scene along West Broadway. South Boston is known for its strong community spirit and hosts several notable events, including the annual St. Patrick's Day Parade. With excellent transportation options, including proximity to South Station, Boston Logan International Airport, and walkable streets, Southie offers a unique blend of historic charm and modern convenience, making it an attractive neighborhood for those seeking a dynamic urban lifestyle with a touch of coastal living.""",
        """ Boston's South End is a vibrant and culturally diverse neighborhood known for its artistic flair, culinary scene, and historic charm. Located between Back Bay and Chinatown, this area is characterized by its elegant Victorian row houses and iconic brownstones, creating a quintessential Boston aesthetic. The SoWa Art + Design District is the heart of the neighborhood's creative spirit, hosting numerous galleries, studios, and events like the popular SoWa Open Market. South End boasts an impressive array of landmark restaurants, trendy cafes, and bars, making it a foodie's paradise. With its proximity to several universities and medical centers, the area maintains a youthful energy while also attracting professionals. The neighborhood is highly walkable and dog-friendly, with numerous parks and green spaces scattered throughout. South End's rich LGBTQ history, annual events like the Boston Pride Parade, and its convenient location near downtown Boston make it an attractive destination for residents seeking a dynamic urban lifestyle with a strong sense of community.""",
        """ Back Bay, one of Boston's most prestigious neighborhoods, offers elegant urban living in the heart of the city. Known for its iconic Victorian-era brownstones and tree-lined streets, Back Bay seamlessly blends historic charm with modern sophistication. The area is a shopper's paradise, featuring the renowned Newbury Street, Prudential Center, and Copley Place. Surrounded by green spaces like the Charles River Esplanade, Boston Public Garden, and Commonwealth Avenue Mall, residents enjoy a peaceful retreat within the bustling metropolis. Back Bay's central location provides easy access to top-rated schools, world-class medical facilities, and efficient public transportation. With its architectural significance, vibrant dining scene, and proximity to cultural attractions, Back Bay attracts a diverse mix of professionals, families, and students seeking a quintessential Boston experience. This highly walkable neighborhood offers a perfect balance of urban amenities and residential tranquility, making it one of the most desirable areas in the city."""
        ],
        "WALK_SCORE": ["95/100", "90/100", "98/100", "100/100"],
        "TRANSIT_SCORE": ["91/100", "48/100", "85/100", "91/100"]
        }

        neighborhood_df = pd.DataFrame(data_neighborhood)
        #insert_zipcodes(neighborhood_df)

        # Insert Open Space
        query = "SELECT * FROM TEMP_OPEN_SPACE_GROUND"
        parks_df = pd.read_sql(query, conn)
        parks_df['ZIP_CODE'] = parks_df['ZIP_CODE'].astype(str).str.zfill(5)
        #insert_parks(parks_df)

        # Insert Subway
        query = "SELECT * FROM SUBWAY"
        subway_df = pd.read_sql(query, conn)
        #insert_subway(subway_df)

        # Insert Restaurant
        query = "SELECT * FROM RESTAURANTS"
        restaurants_df = pd.read_sql(query, conn)
        #insert_restaurants(restaurants_df)

        # Insert Census
        query = "SELECT * FROM BOSTON_CENSUS"
        census_df = pd.read_sql(query, conn)
        demographics = [
        """{
            "High School Graduates": "91.1%",
            "College Graduates": "66.2%",
            "Significantly above the national average": "34.1%",
            "Advanced Degrees": "35.2%",
            "Above the national average": "13.3%",
            "% Population in Labor Force": "55.2%"
        }""",
        """{
            "High School Graduates": "97.9%",
            "College Graduates": "86.4%",
            "Significantly above the national average": "34.1%",
            "Advanced Degrees": "47.8%",
            "Significantly above the national average": "13.3%",
            "% Population in Labor Force": "68.8%"
        }""",
        """{
            "High School Graduates": "83.9%",
            "College Graduates": "55.7%",
            "Above the national average": "34.1%",
            "Advanced Degrees": "28.9%",
            "Above the national average": "13.3%",
            "% Population in Labor Force": "68.3%"
        }""",
        """{
            "High School Graduates": "90.9%",
            "College Graduates": "63.4%",
            "Significantly above the national average": "34.1%",
            "Advanced Degrees": "21.6%",
            "Above the national average": "65.3%",
            "% Population in Labor Force": "83.3%"
        }"""
        ]
        census_df['DEMOGRAPHICS_EDUCATION_WORKFORCE'] = demographics
        #print(census_df)
        #insert_census(census_df)

        ################# ADD code to insert Utilities #######################
        query = "SELECT * FROM UTILITIES"
        utilities_df = pd.read_sql(query, conn)
        #insert_utilities(utilities_df)
        
        ################# ADD code to insert Crimes #######################
        query = "SELECT * FROM CRIME"
        crime_df = pd.read_sql(query, conn)
        #insert_crimes(crime_df)

        # Insert groups
        query = "SELECT * FROM MEETUP_GROUPS"
        groups_df = pd.read_sql(query, conn)
        groups_df['DESCRIPTION_VECTOR'] = groups_df.apply(generate_embeddings, axis=1) ############################ Add Embedding ########################
        print(groups_df)
        #insert_meetup_groups(groups_df)

        # Insert Appartments
        query = "SELECT * FROM APARTMENTS"
        apartments_df = pd.read_sql(query, conn)
        #insert_apartments(apartments_df)
        
        
        ########### Add Code to Insert Violations ########################


        ################## Insert Nearby Restaurants & Parks & Subways ######################

        query = "SELECT * FROM APARTMENTS"
        apartments_df = pd.read_sql(query, conn)

        query = "SELECT * FROM RESTAURANTS"
        restaurants_df = pd.read_sql(query, conn)

        query = "SELECT * FROM SUBWAY"
        subway_df = pd.read_sql(query, conn)

        query = "SELECT * FROM TEMP_OPEN_SPACE_GROUND"
        parks_df = pd.read_sql(query, conn)
        parks_df['ZIP_CODE'] = parks_df['ZIP_CODE'].astype(str).str.zfill(5)

        apartments_df['APT_ZPID'] = apartments_df['APT_ZPID'] +'--'+ apartments_df['APT_UNIT_NUMBER'].astype(str)
        #apartments_df = apartments_df[:3]


        ### Restaurant
        #create_nearby_restaurant_relationship(apartments_df, restaurants_df)
        

        ### Park
        #create_nearby_park_relationship(apartments_df, parks_df)

        ### Subway
        #create_nearby_subway_relationship(apartments_df, subway_df)

        ############################


    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close
        conn.close()

if __name__ == "__main__":
    main()
