from neo4j import GraphDatabase

# Replace with your Neo4j Aura connection details
URI = "neo4j+s://6f4de360.databases.neo4j.io:7687"
AUTH = ("neo4j", "yVsGWUmODVg0hAFAioEcWSLdzgFpQAO7k6kD2mjpOoE")

# Create a Neo4j driver instance
driver = GraphDatabase.driver(URI, auth=AUTH)

# Verify the connection
try:
    with driver.session() as session:
        result = session.run("RETURN 1")
        print("Connection to the database was successful.")
except Exception as e:
    print(f"Error connecting to the database: {e}")
finally:
    # Close the driver connection when done
    driver.close()
