
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re


load_dotenv()

class Neo4jConnection:
    def __init__(self, uri, username, password):
        self.uri = "neo4j+s://6f4de360.databases.neo4j.io:7687"
        self.username = "neo4j"
        self.password = "yVsGWUmODVg0hAFAioEcWSLdzgFpQAO7k6kD2mjpOoE"
        self.driver = None
        self.connect()

    def connect(self):
        """Establish the connection to the Neo4j database."""
        if not self.driver:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.username, self.password))
            print("Connected to Neo4j.")

    def close(self):
        """Close the connection to the Neo4j database."""
        if self.driver:
            self.driver.close()
            print("Connection closed.")

    def run_query(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(query, parameters or {})
            return result

def get_top_meetup_groups(driver, user_vector, top_n=3):
    with driver.session() as session:
        # Fetch MeetupGroup nodes
        result = session.run("""
            MATCH (m:MeetupGroup)
            RETURN m.meetup_group_name AS group_name, 
                   m.meetup_group_description AS description, 
                   m.meetup_group_past_events AS past_events, 
                   m.meetup_group_member_count AS member_count,
                   m.meetup_group_link AS meetup_group_link,
                   m.meetup_group_description_vector AS description_vector
        """)

        groups = []
        for record in result:
            groups.append({
                "group_name": record["group_name"],
                "description": record["description"],
                "past_events": record["past_events"],
                "member_count": record["member_count"],
                "meetup_group_link": record["meetup_group_link"],
                "description_vector": np.array(record["description_vector"], dtype=np.float32) 
            })

        # Calculate cosine similarity
        user_vector_np = np.array(user_vector, dtype=np.float32).reshape(1, -1) 
        similarities = []

        for group in groups:
            group_vector = group["description_vector"].reshape(1, -1)  
            similarity = cosine_similarity(user_vector_np, group_vector)[0][0]
            similarities.append({**group, "similarity": similarity})

        # Sort by similarity
        top_groups = sorted(similarities, key=lambda x: x["similarity"], reverse=True)[:top_n]

        return top_groups
    
def generate_embeddings(user_text):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return model.encode(user_text)

def format_past_events(events_str):
    events = events_str.split(', ')
    
    # Extract and format the event name and date using regex
    formatted_events = []
    for event in events:
        match = re.match(r'(.+?)ID\(Date: (\d{4}-\d{2}-\d{2})\)', event)
        if match:
            event_name = match.group(1).strip()  
            event_date = match.group(2)  
            formatted_events.append(f"{event_name} ({event_date})")
    
    return formatted_events

def get_groups_for_user(user_text):
    uri = os.getenv("NEO4J_URI")
    username = os.getenv("NEO4J_USERNAME")
    password = os.getenv("NEO4J_PASSWORD")

    driver = Neo4jConnection(uri, username, password).driver

    user_vector = generate_embeddings(user_text)

    top_groups = get_top_meetup_groups(driver, user_vector)

    Neo4jConnection(uri, username, password).close()

    meetup_results = [
    {
        "meetup_group_name": group['group_name'],
        "meetup_group_description": group['description'],
        "meetup_group_link": group['meetup_group_link'],
        "meetup_group_member_count": group['member_count'],
        "meetup_group_past_events": format_past_events(group['past_events'])
    }
    for group in top_groups
    ]

    return meetup_results


if __name__ == "__main__":
    user_text = 'Boston Gaymers is a social group for LGBTQIA+ gamers in the Greater Boston area to help find and make new friends.'
    meetup_results = get_groups_for_user(user_text)

    for result in meetup_results:
        print(result)