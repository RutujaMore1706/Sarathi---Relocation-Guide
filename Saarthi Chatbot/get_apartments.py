from neo4j import GraphDatabase
import requests
from neo4j.exceptions import CypherSyntaxError
import re
import pandas as pd
import os ,json, logging


def connect_to_graph_db(uri, auth):
    driver = GraphDatabase.driver(uri, auth=auth)
    verify_connection(driver)
    return driver

def verify_connection(driver):
    with driver.session() as session:
        try:
            session.run("RETURN 1")  # Simple query to check connection
            print("Connection to the database was successful.")
        except Exception as e:
            print(f"Error connecting to the database: {e}")

def close_graph_db(driver):
    driver.close()

def fetch_schema(driver):
    schema_info = {"Nodes": [], "Relationships": []}

    with driver.session() as session:
        # Fetch node labels and properties
        nodes_result = session.run("CALL apoc.meta.schema()")
        for record in nodes_result:
            schema = record["value"]
            for node, details in schema.items():
                if details.get("type") == "node":
                    schema_info["Nodes"].append({
                        "label": node,
                        "properties": list(details["properties"].keys())
                    })
                elif details.get("type") == "relationship":
                    schema_info["Relationships"].append({
                        "type": node,
                        "properties": list(details["properties"].keys())
                    })
    return schema_info

def format_schema_text(schema):
    schema_text = "Nodes:\n"
    for node in schema["Nodes"]:
        schema_text += f" - {node['label']} with properties {node['properties']}\n"

    schema_text += "\nRelationships:\n"
    for rel in schema["Relationships"]:
        schema_text += f" - {rel['type']} with properties {rel['properties']}\n"
    return schema_text

def validate_query_with_schema(cypher_query, valid_nodes):
    for node in valid_nodes:
        if node not in cypher_query:
            # Strip out or ignore parts referencing non-existent nodes
            cypher_query = re.sub(rf"\b{node}\b", "", cypher_query, flags=re.IGNORECASE)

    return cypher_query

def extract_area_from_description(description, areas):
    # Loop through the dictionary to check if the area is mentioned in the user input
    for area_name, postal_code in areas.items():
        if area_name.lower() in description.lower():
            return postal_code
    return None  # Return None if no area is found

def construct_llm_prompt(description, schema, areas):
    schema_text = format_schema_text(schema)
    
    areas = {
        "fenway": "02215",
        "south boston": "02216",
        "south end": "02118",
        "back bay": "02116",
    }
    # Extract area from description using the areas dictionary
    area_postal_code = extract_area_from_description(description, areas)

    prompt = f"""
               User Input: {description}

                Task: You are a Neo4J and Cypher expert. Generate a Cypher query to find the top 4 apartments based on the provided schema and user input.

                ### Rules:
                DO NOT ASSUME ANYTHING, USE ONLY THE INFORMATION GIVEN IN User Input. Do not under any circumstances create new relationships.
                1. Use nodes, labels, and properties ONLY from {schema_text}. For locations, use postal codes from {area_postal_code}.
                2. Start with MATCH (a:Apartment). and make sure all Match statements are at the top before Where clause.
                3. Always alias relationships in MATCH. Do not embed relationship properties directly in patterns. instead 
                   - Match relationships and assign them aliases 
                   - Filter properties in the WHERE clause using the aliases.
                4. For strings with units, use toInteger(split(alias.prop, ' ')[0]) for comparisons as neo4j has data in km and mins.
                5. Ensure the query ends with `RETURN DISTINCT a ORDER BY a.apt_rent LIMIT 4
                """

    return prompt


def call_llm_api(prompt):
    openai_api_key = os.getenv("OPENAI_API_KEY")
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {openai_api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "gpt-4-turbo",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an advanced chatbot specializing in writing Cypher queries to "
                    "fetch data from the Neo4j graph database. You follow all syntax thoroughly "
                    "and do not assume any syntax on your own. Your job is to be precise and concise. "
                    "Every mistake you make, the customer stops using your app."
                )
            },
            {"role": "user", "content": prompt}
        ],
    }
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        response_text = response.json()["choices"][0]["message"]["content"]
         # Clean up the response to extract only the Cypher query
        match = re.search(r'```cypher(.*?)```', response_text, re.DOTALL)
        if match:
            return match.group(1).strip()  # Extract the Cypher query without extra text
        else:
            raise ValueError("No Cypher query found in the response.")
    else:
        raise Exception(f"Error from LLM API: {response.status_code} {response.text}")
  
def query_database(driver, cypher_query, params={}):
    schema = fetch_schema(driver)
    valid_nodes = [node['label'] for node in schema["Nodes"]]
    
    clean_query = validate_query_with_schema(cypher_query, valid_nodes)
    clean_query = cypher_query.replace("```cypher", "").replace("```", "").strip().split(';')[0].strip()
    print("------------------------------------")
    print(" Cleaned query ",clean_query)
    
    # Check for any destructive keywords
    destructive_keywords = ["DELETE", "DETACH DELETE", "DROP", "CREATE", "SET", "MERGE", "REMOVE"]
    if any(re.search(rf"\b{keyword}\b", clean_query, re.IGNORECASE) for keyword in destructive_keywords):
        raise ValueError("Query contains schema-altering or destructive operations and is not allowed.")

    with driver.session() as session:
        result = session.run(clean_query, params)
        # return [dict(record) for record in result]
        raw_result = [record for record in result]
        print("------------------------------------")
        print("Raw query result:", raw_result)
        return raw_result

def extract_properties(query_result):
    data = []
    for record in query_result:
        # Assume the 'a' field contains the node with properties
        node = record["a"]
        properties = node._properties  # Access the properties dictionary
        data.append(properties)
    return data

def node_to_dict(node):
    return dict(node.items())

# def record_to_dict(record):
#     result = {
#         "apt_zpid": record["apt_zpid"],
#         "apt_address": record["apt_address"],
#         "nearest_parks": [
#             {
#                 "walking_time": park["walking_time"],
#                 "distance": park["distance"],
#                 "park": node_to_dict(park["park"])
#             } for park in record["nearest_parks"]
#         ],
#         "nearest_restaurants": [
#             {
#                 "walking_time": restaurant["walking_time"],
#                 "distance": restaurant["distance"],
#                 "restaurant": node_to_dict(restaurant["restaurant"])
#             } for restaurant in record["nearest_restaurants"]
#         ],
#         "nearest_subways": [
#             {
#                 "walking_time": subway["walking_time"],
#                 "distance": subway["distance"],
#                 "subway": node_to_dict(subway["subway"])
#             } for subway in record["nearest_subways"]
#         ]
#     }
#     return result
def record_to_dict(records):
    results = []
    for record in records:
        if record:  # Check if the record is not empty
            apartment = record[0]  # Assuming the first item is the apartment data
            result = {
                "apt_zpid": apartment["apt_zpid"],
                "apt_address": apartment["apt_address"],
                "nearest_parks": [
                    {
                        "walking_time": park["walking_time"],
                        "distance": park["distance"],
                        "park": node_to_dict(park["park"])
                    } for park in apartment["nearest_parks"]
                ],
                "nearest_restaurants": [
                    {
                        "walking_time": restaurant["walking_time"],
                        "distance": restaurant["distance"],
                        "restaurant": node_to_dict(restaurant["restaurant"])
                    } for restaurant in apartment["nearest_restaurants"]
                ],
                "nearest_subways": [
                    {
                        "walking_time": subway["walking_time"],
                        "distance": subway["distance"],
                        "subway": node_to_dict(subway["subway"])
                    } for subway in apartment["nearest_subways"]
                ]
            }
            results.append(result)
    return results


def run_query(uri, auth, openai_api_key, description):
    areas = {
        "fenway": "02215",
        "south boston": "02216",
        "south end": "02118",
        "back bay": "02116",
    }

    # Use a connection pool instead of creating a new connection each time
    with GraphDatabase.driver(uri, auth=auth) as driver:
        schema = fetch_schema(driver)
        prompt = construct_llm_prompt(description, schema, areas)
        cypher_query = call_llm_api(prompt)
        
        try:
            query_result = query_database(driver, cypher_query)
            data = extract_properties(query_result)
            apartments_json_result = json.dumps(data, indent=2)
            
            cypher_query_for_nearby_places = get_nearby_places(data)
            nearby_places = [query_database(driver, query) for query in cypher_query_for_nearby_places]
            # print("------------------------------")
            # print(nearby_places)

            # Convert the record to a dictionary
            nearby_places_data = record_to_dict(nearby_places)

            # Convert the dictionary to JSON
            nearby_places_json_data = json.dumps(nearby_places_data, indent=4)

            # Print or save the JSON data
            # print(nearby_places_json_data)
            
            return apartments_json_result, nearby_places_json_data
        except Exception as e:
            logging.error(f"Error in run_query: {str(e)}")
            raise

def get_nearby_places(apartments):
    cypher_queries = []
    for apt in apartments:
        query = f"""
        MATCH (a:Apartment {{apt_zpid: '{apt["apt_zpid"]}'}})
        
        // Find nearest parks
        OPTIONAL MATCH (a)-[r1:has_nearby_park]->(p:Park)
        WITH a, p, r1
        ORDER BY r1.distance ASC
        LIMIT 3
        WITH a, COLLECT({{park: p, distance: r1.distance, walking_time: r1.walking_time}}) AS nearest_parks
        
        // Find nearest restaurants
        OPTIONAL MATCH (a)-[r2:has_nearby_restaurant]->(r:Restaurant)
        WITH a, nearest_parks, r, r2
        ORDER BY r2.distance ASC
        LIMIT 3
        WITH a, nearest_parks, COLLECT({{restaurant: r, distance: r2.distance, walking_time: r2.walking_time}}) AS nearest_restaurants
        
        // Find nearest subway stations
        OPTIONAL MATCH (a)-[r3:has_nearby_subwaystation]->(s:Subway)
        WITH a, nearest_parks, nearest_restaurants, s, r3
        ORDER BY r3.distance ASC
        LIMIT 3
        WITH a, nearest_parks, nearest_restaurants, COLLECT({{subway: s, distance: r3.distance, walking_time: r3.walking_time}}) AS nearest_subways
        
        RETURN a.apt_zpid AS apt_zpid, 
               a.apt_address AS apt_address, 
               nearest_parks, 
               nearest_restaurants, 
               nearest_subways
        """
        cypher_queries.append(query)
    return cypher_queries

def format_apartment_data(data):
    apartments = json.loads(data[0])
    nearby_places = json.loads(data[1])

    formatted_output = []

    for apt, places in zip(apartments, nearby_places):
        formatted_apt = {
            "Apartment": {
                "apt_address": apt["apt_address"],
                "apt_unit":apt["apt_unit"],
                "apt_building_name": f"{apt['apt_building_name']}" if apt['apt_building_name'] else "Not available",
                "apt_rent": f"${apt['apt_rent']}",
                "apt_bedroom_count": apt["apt_bedroom_count"],
                "apt_bathroom_count": apt["apt_bathroom_count"],
                "apt_living_area": f"{apt['apt_living_area']} sq ft" if apt['apt_living_area'] else "Not available",
                "apt_transit_score Score": apt["apt_transit_score"],
                "apt_latitude":apt["apt_latitude"],
                "apt_longitude": apt["apt_longitude"],
                "apt_url":  f"{apt['apt_url']}" if apt['apt_url'] else "Not available",
                "apt_image_url":f"{apt['apt_image_url']}" if apt['apt_image_url'] else "Not available",
            },
            "Nearby Places": {
                "Parks": [
                    {
                        "openspace_name": park["park"]["openspace_name"],
                        "openspace_type": park["park"]["openspace_type"],
                        "distance": park["distance"],
                        "walking_time Time": park["walking_time"]
                    } for park in places["nearest_parks"]
                ],
                "Restaurants": [
                    {
                        "restaurant_name": restaurant["restaurant"]["restaurant_name"],
                        "restaurant_cuisine": restaurant["restaurant"]["restaurant_cuisine"],
                        "restaurant_rating": restaurant["restaurant"]["restaurant_rating"],
                        "distance": restaurant["distance"],
                        "walking_time Time": restaurant["walking_time"],
                        "restaurant_url":restaurant["restaurant"]["restaurant_url"]
                    } for restaurant in places["nearest_restaurants"]
                ],
                "Subway Stations": [
                    {
                        "subway_station_name": subway["subway"]["subway_station_name"],
                        "subway_line": subway["subway"]["subway_line"],
                        "subway_route": subway["subway"]["subway_route"],
                        "distance": subway["distance"],
                        "walking_time": subway["walking_time"]
                    } for subway in places["nearest_subways"]
                ]
            }
        }
        formatted_output.append(formatted_apt)

    return json.dumps(formatted_output, indent=2)


def get_data_from_graph(extracted_preference):
    openai_key = "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"
    neo4j_URI = "neo4j+ssc://6f4de360.databases.neo4j.io:7687"
    neo4j_AUTH = ("neo4j", "yVsGWUmODVg0hAFAioEcWSLdzgFpQAO7k6kD2mjpOoE")
   
    preference_summary = extracted_preference
    results = run_query(neo4j_URI, neo4j_AUTH, openai_key, preference_summary)
    formatted_json = format_apartment_data(results)
    return formatted_json


def separate_summary_and_hobbies(text):
    lines = text.strip().split("\n")
    summary = None
    hobbies = None

    for line in lines:
        if line.startswith("Summary:"):
            summary = line.replace("Summary:", "").strip()
        elif line.startswith("Hobbies:"):
            hobbies = line.replace("Hobbies:", "").strip()

    return summary, hobbies



# if __name__ == "__main__":
#    main()
    
    
    


