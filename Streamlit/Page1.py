import streamlit as st
from streamlit_chat import message
from neo4j import GraphDatabase

# Initialize the app
st.set_page_config(page_title="Saarthi-Boston", layout="wide")

# Sidebar for navigation
st.sidebar.title("Saarthi-Boston Chatbots")
selected_chatbot = st.sidebar.radio(
    "Select Chatbot:",
    options=["User Profile", "Suggest Neighborhood"]
)

# Initialize session state for both chatbots
if "user_profile" not in st.session_state:
    st.session_state.user_profile = {"name": None, "age": None, "new_to_boston": None, "reason": None, "address": None}

if "neighborhood_data" not in st.session_state:
    st.session_state.neighborhood_data = None

# Neo4j connection setup (replace with your credentials)
def connect_to_neo4j(uri, user, password):
    return GraphDatabase.driver(uri, auth=(user, password))

# Fetch data from Knowledge Graph
def get_neighborhoods(city="Boston"):
    uri = "neo4j+s://<your_neo4j_instance_uri>"  # Replace with your instance URI
    user = "<username>"
    password = "<password>"
    query = """
    MATCH (n:Neighborhood)-[:LOCATED_IN]->(c:City {name: $city})
    RETURN n.name AS neighborhood
    """
    with connect_to_neo4j(uri, user, password) as driver:
        with driver.session() as session:
            result = session.run(query, city=city)
            return [record["neighborhood"] for record in result]

# Chatbot: User Profile
if selected_chatbot == "User Profile":
    st.title("👤 User Profile Builder")
    st.write("Let's build your profile!")

    # Ask for name
    name = st.text_input("What's your name?", value=st.session_state.user_profile["name"] or "")
    if name:
        st.session_state.user_profile["name"] = name

    # Ask for age
    age = st.number_input("How old are you?", min_value=0, value=st.session_state.user_profile["age"] or 0)
    if age:
        st.session_state.user_profile["age"] = age

    # Ask if new to Boston
    new_to_boston = st.radio(
        "Are you new to Boston?",
        options=["Yes, I'm new", "No, I live here already"],
        index=0 if st.session_state.user_profile["new_to_boston"] == "Yes, I'm new" else 1
    )
    if new_to_boston:
        st.session_state.user_profile["new_to_boston"] = new_to_boston

    # If new, ask for reason and address
    if new_to_boston == "Yes, I'm new":
        reason = st.text_input("What brings you here? (e.g., University, Job)", value=st.session_state.user_profile["reason"] or "")
        if reason:
            st.session_state.user_profile["reason"] = reason

        address = st.text_area("Enter your office or university address:", value=st.session_state.user_profile["address"] or "")
        if address:
            st.session_state.user_profile["address"] = address

    # Display user profile summary
    if st.button("Show My Profile"):
        st.write("### Your Profile Summary")
        st.write(st.session_state.user_profile)

# Chatbot: Suggest Neighborhood
# elif selected_chatbot == "Suggest Neighborhood":
#     st.title("📍 Neighborhood Suggestions")
#     st.write("Based on your profile, here are some neighborhoods in Boston:")

#     # Check if user profile is available
#     if not st.session_state.user_profile["name"]:
#         st.write("⚠️ Please complete your user profile first.")
#     else:
#         if st.session_state.neighborhood_data is None:
#             st.session_state.neighborhood_data = get_neighborhoods()

#         # Display neighborhoods
#         for neighborhood in st.session_state.neighborhood_data:
#             st.write(f"- {neighborhood}")

elif selected_chatbot == "Suggest Neighborhood":
    st.title("📍 Neighborhood Suggestions")
    st.write("Explore neighborhoods in Boston to find your perfect match!")

    # Define neighborhoods and their corresponding URLs
    # neighborhoods = {
    #     "Fenway-Kenmore": "https://www.meetboston.com/explore/neighborhoods/fenway-kenmore/",
    #     "Back Bay": "https://www.meetboston.com/explore/neighborhoods/back-bay/",
    #     "South End": "https://www.meetboston.com/explore/neighborhoods/south-end/",
    #     "Beacon Hill": "https://www.meetboston.com/explore/neighborhoods/beacon-hill/",
    #     "North End": "https://www.meetboston.com/explore/neighborhoods/north-end/",
    # }

    # Define neighborhoods, summaries, and URLs
    neighborhoods = {
        "Fenway-Kenmore": {
            "summary": "Known for Fenway Park and a vibrant college town vibe, this neighborhood is home to cultural landmarks, restaurants, and lively nightlife.",
            "url": "https://www.meetboston.com/explore/neighborhoods/fenway-kenmore/"
            # "video": "https://www.homes.com/local-guide/boston-ma/fenway-neighborhood/?tab=0&dk=zdn70fvfek44z"

        },
        "Back Bay": {
            "summary": "A mix of historic charm and urban luxury, Back Bay boasts iconic brownstones, Newbury Street shopping, and the scenic Charles River Esplanade.",
            "url": "https://www.meetboston.com/explore/neighborhoods/back-bay/"
        },
        "South End": {
            "summary": "A hub for foodies and art enthusiasts, South End is known for its trendy restaurants, art galleries, and Victorian-style row houses.",
            "url": "https://www.meetboston.com/explore/neighborhoods/south-end/"
        },
        "Beacon Hill": {
            "summary": "Beacon Hill is Boston's quintessential historic district with cobblestone streets, gaslit lamps, and picturesque Federal-style townhouses.",
            "url": "https://www.meetboston.com/explore/neighborhoods/beacon-hill/"
        },
        "North End": {
            "summary": "Boston's oldest residential neighborhood, North End is famous for its Italian heritage, dining spots, and historic sites like Paul Revere's House.",
            "url": "https://www.meetboston.com/explore/neighborhoods/north-end/"
        },
    }

    # Display each neighborhood as an expander with a summary and embedded website
    # for name, info in neighborhoods.items():
    #     with st.expander(name):
    #         # Show summary
    #         st.write(f"**Summary:** {info['summary']}")
    #         st.write("Explore more about this neighborhood below:")
            
    #         # Embed the corresponding neighborhood page
    #         st.components.v1.iframe(src=info["url"], height=500, scrolling=True)
    for name, info in neighborhoods.items():
        with st.expander(name):
            # Show summary
            st.write(f"{info['summary']}")

            st.write("Explore more about this neighborhood below:")
            
            # Embed the corresponding neighborhood page
            st.components.v1.iframe(src=info["url"], height=500, scrolling=True)
