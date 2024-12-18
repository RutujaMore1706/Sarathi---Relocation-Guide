from neo4j import GraphDatabase
import googlemaps
import pandas as pd
import json

# Replace with your Neo4j Aura connection details
URI = "neo4j+s://6f4de360.databases.neo4j.io:7687"  
AUTH = ("neo4j", "yVsGWUmODVg0hAFAioEcWSLdzgFpQAO7k6kD2mjpOoE")

class GraphDB:
    def __init__(self, uri, auth):
        self.driver = GraphDatabase.driver(uri, auth=auth)
        self.verify_connection()

    def verify_connection(self):
        # Verify connectivity to the database
        with self.driver.session() as session:
            try:
                session.run("RETURN 1")  # Simple query to check connection
                print("Connection to the database was successful.")
            except Exception as e:
                print(f"Error connecting to the database: {e}")

    def close(self):
        self.driver.close()

    def create_zipcode(self, zipcode, neighborhood, summary, walk_score, transit_score):
        with self.driver.session() as session:
            session.run("""CREATE (z:Zipcode {
                        zipcode: $zipcode,
                        neighborhood_name: $neighborhood,
                        neighborhood_summary: $summary,
                        neighborhood_walk_score: $walk_score,
                        neighborhood_transit_score: $transit_score
                        })""", zipcode=zipcode, neighborhood = neighborhood, summary = summary, walk_score = walk_score, transit_score = transit_score)

    def create_apartment(self, zpid, address, bedroom_count, bathroom_count, rent, living_area, transit_score, latitude, longitude, url, image_url, zipcode, building_name, lot_id, property_type, unit):
        with self.driver.session() as session:
            session.run("""
                CREATE (a:Apartment {
                    apt_zpid: $zpid,
                    apt_address: $address, 
                    apt_bedroom_count: $bedroom_count, 
                    apt_bathroom_count: $bathroom_count,
                    apt_rent: $rent, 
                    apt_living_area: $living_area, 
                    apt_transit_score: $transit_score,
                    apt_latitude: $latitude, 
                    apt_longitude: $longitude, 
                    apt_url: $url, 
                    apt_image_url: $image_url,
                    apt_zip_code: $zipcode,
                    apt_building_name: $building_name,
                    apt_lot_id: $lot_id,
                    apt_property_type: $property_type,
                    apt_unit: $unit
                })
                WITH a
                MATCH (z:Zipcode {zipcode: $zipcode})
                CREATE (a)-[:is_in_zipcode]->(z)
            """, zpid=zpid, address=address, bedroom_count=bedroom_count, bathroom_count=bathroom_count, 
                rent=rent, living_area=living_area, transit_score=transit_score,
                latitude=latitude, longitude=longitude, url=url, image_url=image_url, zipcode=zipcode, building_name=building_name, lot_id=lot_id, property_type=property_type, unit=unit)

    def create_census(self, zipcode, population, hispanic_latino, white, black, american_indian, asian, native_hawaiian, some_other_race, demographics_education_workforce):
        with self.driver.session() as session:
            session.run("""
                CREATE (c:Census {
                    zipcode: $zipcode, 
                    population: $population, 
                    hispanic_latino: $hispanic_latino,
                    white: $white,
                    black: $black,
                    american_indian: $american_indian,
                    asian: $asian,
                    native_hawaiian: $native_hawaiian,
                    some_other_race: $some_other_race,
                    demographics_education_workforce: $demographics_education_workforce
                })
                WITH c
                MATCH (z:Zipcode {zipcode: $zipcode})
                CREATE (z)-[:has_Census]->(c)
            """, zipcode=zipcode, population=population, 
            hispanic_latino=hispanic_latino,
            white=white,
            black=black,
            american_indian=american_indian,
            asian=asian,
            native_hawaiian=native_hawaiian,
            some_other_race=some_other_race,
            demographics_education_workforce=demographics_education_workforce)

    '''
    def create_utilities(self, zipcode, category, total_cost):
        with self.driver.session() as session:
            session.run("""
                CREATE (u:Utilities {
                    zipcode: $zipcode, category: $category, total_cost: $total_cost
                })
                WITH u
                MATCH (z:Zipcode {zipcode: $zipcode})
                CREATE (z)-[:has_Utilities]->(u)
            """, zipcode=zipcode, category=category, total_cost=total_cost)
    '''
    def create_utilities(self, zipcode, electric, natural_gas, steam, water, total_cost):
        with self.driver.session() as session:
            session.run("""
                CREATE (u:Utilities {
                    zipcode: $zipcode, 
                    electricity_bill: $electric,
                    gas_bill: $natural_gas,
                    heat_bill: $steam,
                    water_bill: $water, 
                    total_bill: $total_cost
                })
                WITH u
                MATCH (z:Zipcode {zipcode: $zipcode})
                CREATE (z)-[:has_Utilities]->(u)
            """, zipcode=zipcode, electric=electric, natural_gas = natural_gas, steam = steam, water = water, total_cost=total_cost)

    def create_crime(self, zipcode, detail, area_stat, national_average):
        with self.driver.session() as session:
            session.run("""
                CREATE (c:Crime {
                    crime_zipcode: $zipcode, 
                    crime_detail: $detail, 
                    crime_area_stat: $area_stat,
                    crime_national_average: $national_average
                    
                })
                WITH c
                MATCH (z:Zipcode {zipcode: $zipcode})
                CREATE (z)-[:has_Crime]->(c)
            """, zipcode=zipcode, detail=detail, area_stat=area_stat, national_average = national_average)

    def create_park(self, name, address, acreage, type_, zipcode):
        with self.driver.session() as session:
            session.run("""
                CREATE (p:Park {
                    openspace_name: $name,
                    openspace_address: $address, 
                    openspace_acreage: $acreage, 
                    openspace_type: $type, 
                    openspace_zipcode: $zipcode
                })
                WITH p
                MATCH (z:Zipcode {zipcode: $zipcode})
                CREATE (z)-[:has_Parks]->(p)
            """, name=name, address=address, acreage=acreage, type=type_, zipcode=zipcode)
    
    def create_subway(self, name, line, route, zipcode, latitude, longitude):
        with self.driver.session() as session:
            session.run("""
                CREATE (s:Subway {
                    subway_station_name: $name,
                    subway_line: $line, 
                    subway_route: $route, 
                    subway_zip_code: $zipcode, 
                    subway_latitude: $latitude,
                    subway_longitude: $longitude
                    
                })
                WITH s
                MATCH (z:Zipcode {zipcode: $zipcode})
                CREATE (z)-[:has_SubwayStation]->(s)
            """, name=name, line=line, route=route, zipcode=zipcode, latitude=latitude, longitude=longitude)
    '''
    def create_restaurant(self, name, cuisine, address, latitude, longitude, zipcode):
        with self.driver.session() as session:
            session.run("""
                CREATE (r:Restaurant {
                    name: $name, cuisine: $cuisine, address: $address,
                    latitude: $latitude, longitude: $longitude
                })
                WITH r
                MATCH (z:Zipcode {zipcode: $zipcode})
                CREATE (z)-[:has_Restaurants]->(r)
            """, name=name, cuisine=cuisine, address=address, latitude=latitude, longitude=longitude, zipcode=zipcode)
    '''
    
    def create_restaurant(self, id, name, cuisine, url, image_url, price, rating, latitude, longitude, address, zipcode):
        with self.driver.session() as session:
            session.run("""
                CREATE (r:Restaurant {
                    restaurant_id: $id,
                    restaurant_name: $name, 
                    restaurant_cuisine: $cuisine,
                    restaurant_url: $url,
                    restaurant_image_url: $image_url,
                    restaurant_price: $price,
                    restaurant_rating: $rating, 
                    restaurant_latitude: $latitude, 
                    restaurant_longitude: $longitude,
                    restaurant_address: $address
                })
                WITH r
                MATCH (z:Zipcode {zipcode: $zipcode})
                CREATE (z)-[:has_Restaurants]->(r)
            """, id=id, name=name, cuisine=cuisine, url=url, image_url=image_url, price=price, rating=rating, latitude=latitude, longitude=longitude, address=address, zipcode=zipcode)

    '''
    def create_meetup_group(self, name, description, link, category, sub_category, city, zipcode, member_count, past_events_count):
        with self.driver.session() as session:
            session.run("""
                CREATE (m:MeetupGroup {
                    name: $name, description: $description, link: $link,
                    category: $category, sub_category: $sub_category, city: $city,
                    member_count: $member_count, past_events_count: $past_events_count
                })
                WITH m
                MATCH (z:Zipcode {zipcode: $zipcode})
                CREATE (z)-[:has_Meetup_Groups]->(m)
            """, name=name, description=description, link=link, category=category, 
                sub_category=sub_category, city=city, zipcode=zipcode, 
                member_count=member_count, past_events_count=past_events_count)
    '''

    def create_meetup_group(self, name, description, link, category, city, zipcode, member_count, past_events, description_vector):
        #description_vector_str = json.dumps(description_vector.tolist())
        with self.driver.session() as session:
            session.run("""
                CREATE (m:MeetupGroup {
                    meetup_group_name: $name, 
                    meetup_group_description: $description, 
                    meetup_group_link: $link,
                    meetup_group_category: $category,
                    meetup_group_city: $city,
                    meetup_group_member_count: $member_count,
                    meetup_group_past_events: $past_events,
                    meetup_group_description_vector: $description_vector
                })
                WITH m
                MATCH (z:Zipcode {zipcode: $zipcode})
                CREATE (z)-[:has_Meetup_Groups]->(m)
            """, name=name, description=description, link=link, category=category, city=city, zipcode=zipcode, 
                member_count=member_count, past_events=past_events,
                description_vector=description_vector)

    def create_violation(self, date, violation_type, description, address, neighborhood, zip_code, property_type, latitude, longitude):
        with self.driver.session() as session:
            session.run("""
                    CREATE (v:Violation {
                        apt_address: $address,
                        violation_date: $date, 
                        violation_type: $violation_type, 
                        violation_description: $description,
                        neighborhood: $neighborhood,
                        zip_code: $zip_code,
                        violation_property_type: $property_type,
                        violation_latitude: $latitude,
                        violation_longitude: $longitude
                    })
                    WITH v
                    MATCH (a:Apartment {address: $address})
                    CREATE (a)-[:has_violation]->(v)
                """, date=date, violation_type=violation_type, description=description,
                    address=address, neighborhood=neighborhood, zip_code=zip_code,
                    property_type=property_type, latitude=latitude, longitude=longitude)

    '''
    def create_nearby_restaurant(self, apartment_address, restaurant_name, walking_time, distance):
        with self.driver.session() as session:
            session.run("""
                MATCH (a:Apartment {address: $apartment_address}), (r:Restaurant {name: $restaurant_name})
                CREATE (a)-[:has_nearby_restaurant {
                    walking_time: $walking_time, distance: $distance
                }]->(r)
            """, apartment_address=apartment_address, restaurant_name=restaurant_name,
                walking_time=walking_time, distance=distance)
    '''
    def create_nearby_restaurant(self, apartment_zpid, restaurant_id, walking_time, distance):
        with self.driver.session() as session:
            session.run("""
                MATCH (a:Apartment {apt_zpid: $apartment_zpid}), (r:Restaurant {restaurant_id: $restaurant_id})
                CREATE (a)-[:has_nearby_restaurant {
                    walking_time: $walking_time, distance: $distance
                }]->(r)
            """, apartment_zpid=apartment_zpid, restaurant_id=restaurant_id,
                walking_time=walking_time, distance=distance)
    
    def create_nearby_park(self, apartment_zpid, park_name, walking_time, distance):
        with self.driver.session() as session:
            session.run("""
                MATCH (a:Apartment {apt_zpid: $apartment_zpid}), (p:Park {openspace_name: $park_name})
                CREATE (a)-[:has_nearby_park {
                    walking_time: $walking_time, distance: $distance
                }]->(p)
            """, apartment_zpid=apartment_zpid, park_name=park_name,
                walking_time=walking_time, distance=distance)
    
    def create_nearby_subwaystation(self, apartment_zpid, subway_station_name, walking_time, distance):
        with self.driver.session() as session:
            session.run("""
                MATCH (a:Apartment {apt_zpid: $apartment_zpid}), (s:Subway {subway_station_name: $subway_station_name})
                CREATE (a)-[:has_nearby_subwaystation {
                    walking_time: $walking_time, distance: $distance
                }]->(s)
            """, apartment_zpid=apartment_zpid, subway_station_name=subway_station_name,
                walking_time=walking_time, distance=distance)

# Example usage
if __name__ == "__main__":
    graph = GraphDB(URI, AUTH)

    graph.create_zipcode("12345",'ABRA','SummaryABRA','85/100','99/100')

    graph.create_apartment(123, "123 Main St", 2, 1, 1200, 800, 8, 40.7128, -74.0060, "http://example.com/apartment1", "http://example.com/image1.jpg", "12345",'ABCD', 123, '3bed', 2)
    graph.create_census(zipcode="12345", population=5000, hispanic_latino=15, white=60, black=30, american_indian=2, asian=8, native_hawaiian=1, some_other_race=4, demographics_education_workforce="{'High School Graduates': '91.1%'}")
    graph.create_utilities("12345", 96, 19, 0,  1, 150)
    graph.create_crime("12345", "1 - Low Crime, 10 - High Crime", '{"AssaultWithWeapon": 3,"Burglary": 4,"CrimeScore": 3,"Homicide": 3,"Larceny": 3,"MotorVehicleTheft": 2,"Robbery": 4,"SexualAssault": 4}','{"AssaultWithWeapon": 4,"Burglary": 4,"CrimeScore": 4,"Homicide": 4,"Larceny": 4,"MotorVehicleTheft": 4,"Robbery": 4,"SexualAssault": 4}')
    graph.create_park("Central Park", "59th St & 5th Ave", 843, "Public Park", "12345")
    graph.create_subway('ABC Station', 'ABC Line', 'ABC Route', '12345', 40.1728, -74.0070)
    graph.create_restaurant(
        id=1,
        name="Pasta Palace",
        cuisine="Italian",
        url="http://example.com/pasta-palace",
        image_url="http://example.com/image.jpg",
        price="$$$",
        rating=4.5,
        latitude=42.3601,
        longitude=-71.0589,
        address="123 Pasta St, Boston, MA",
        zipcode="12345"
        )

    graph.create_meetup_group("Coding Meetup", "A group for coding enthusiasts", "http://example.com/meetup", "Programming", "New York", "12345", 50, ["Unicycle Basketball(Date: 2024-08-22)", "General Unicycle Meetup(Date: 2024-08-31)"],[0.12, 0.04, 0.30, 0.07, 0.09, 0.03, 0.21, 0.11, 0.18, 0.05])
    
    graph.create_violation(date="2024-10-01", violation_type="Noise complaint", description="Loud music late at night",
        address="123 Main St",
        neighborhood="Downtown",
        zip_code="12345",
        property_type="Apartment",
        latitude=40.7128,
        longitude=-74.0060
    )

    graph.create_nearby_restaurant(123, 1, "10 minutes", "0.5 miles")
    graph.create_nearby_park(123, "Central Park", "5 minutes", "0.25 miles")
    graph.create_nearby_subwaystation(123, "ABC Station", "6 minutes", "0.35 miles")

    graph.close()
