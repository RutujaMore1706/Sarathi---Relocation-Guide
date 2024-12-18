import streamlit as st
from get_context_data import get_crime_context, get_restaurant_context, get_park_context, get_demographics_context
import re
import pandas as pd
import sys
import os



# Function to identify the intent and extract area/feature
def parse_user_query(query):
    areas = {
        "fenway": "02215",
        "south boston": "02216",
        "south end": "02118",
        "back bay": "02116",
    }
    features = ["crime", "restaurants", "parks", "demographics"]
    
    # Normalize the input for matching
    query = query.lower()
    
    # Match the area
    area = None
    for key in areas:
        if key in query:
            area = key
            break
    
    # Match the feature
    feature = None
    for f in features:
        if f in query:
            feature = f
            break
    
    return areas.get(area), feature


# Function to format and display data
def display_data(feature, data):
    if feature == "crime":
        st.subheader("Crime Details")
        
        if isinstance(data, list) and len(data) > 0:  # Check if data is a list with elements
            crime_data = data[0]  # Access the first dictionary in the list
            
            crime_stats = crime_data.get('areaStats', {})
            national_avg = crime_data.get('nationalAverage', {})
            
            # Extract the crime statistics
            crime_details = {
                "Crime Type": ["Assault with Weapon", "Burglary", "Homicide", "Larceny", "Motor Vehicle Theft", "Robbery", "Sexual Assault"],
                "Crime Score": [
                    crime_stats.get('AssaultWithWeapon', 'N/A'),
                    crime_stats.get('Burglary', 'N/A'),
                    crime_stats.get('Homicide', 'N/A'),
                    crime_stats.get('Larceny', 'N/A'),
                    crime_stats.get('MotorVehicleTheft', 'N/A'),
                    crime_stats.get('Robbery', 'N/A'),
                    crime_stats.get('SexualAssault', 'N/A')
                ],
                "National Average": [
                    national_avg.get('AssaultWithWeapon', 'N/A'),
                    national_avg.get('Burglary', 'N/A'),
                    national_avg.get('Homicide', 'N/A'),
                    national_avg.get('Larceny', 'N/A'),
                    national_avg.get('MotorVehicleTheft', 'N/A'),
                    national_avg.get('Robbery', 'N/A'),
                    national_avg.get('SexualAssault', 'N/A')
                ]
            }

            crime_df = pd.DataFrame(crime_details)
            st.dataframe(crime_df)
        else:
            st.error("Crime data is not in the expected format.")

    elif feature == "restaurants":
        st.subheader("Top Restaurants")
        
        if isinstance(data, list):  # Check if data is a list
            for restaurant in data:
                with st.expander(restaurant.get('restaurantName', 'Unknown Restaurant')):
                    st.write(f"**Rating**: {restaurant.get('rating', 'N/A')}")
                    st.write(f"**Cuisine**: {restaurant.get('cuisine', 'N/A')}")
                    st.write(f"**Price**: {restaurant.get('price', 'N/A')}")
                    st.write(f"**Address**: {restaurant.get('address', 'N/A')}")
                    st.write(f"**URL**: {restaurant.get('url', 'N/A')}")
        else:
            st.error("Restaurants data is not in the expected format.")
    
    elif feature == "parks":
        st.subheader("Top Parks")
        
        if isinstance(data, list):  # Check if data is a list
            for park in data:
                with st.expander(park.get('parkName', 'Unknown Park')):
                    st.write(f"**Type**: {park.get('type', 'N/A')}")
                    st.write(f"**Acreage**: {park.get('acreage', 'N/A')}")
                    st.write(f"**Address**: {park.get('address', 'N/A')}")
        else:
            st.error("Parks data is not in the expected format.")
    
    elif feature == "demographics":
        st.subheader("Demographics")
        
        if isinstance(data, list) and len(data) > 0:  # Check if data is a list with elements
            demographics_data = data[0]  # Access the first dictionary in the list
            
            demographics = {
                "Population": demographics_data.get('population', 'N/A'),
                "White Population": demographics_data.get('white', 'N/A'),
                "Black Population": demographics_data.get('black', 'N/A'),
                "Asian Population": demographics_data.get('asian', 'N/A'),
                "Hispanic/Latino Population": demographics_data.get('hispanicLatino', 'N/A'),
                "American Indian": demographics_data.get('americanIndian', 'N/A'),
                "Native Hawaiian": demographics_data.get('nativeHawaiian', 'N/A'),
            }
            
            demographics_df = pd.DataFrame(list(demographics.items()), columns=["Demographic", "Value"])
            st.table(demographics_df)  

             # Visualizing the population distribution
            racial_data = {
                "Race": ["White", "Black", "Asian", "Hispanic/Latino", "American Indian", "Native Hawaiian", "Other Race"],
                "Population": [
                    int(demographics_data.get('white', 0).replace(',', '')),
                    int(demographics_data.get('black', 0).replace(',', '')),
                    int(demographics_data.get('asian', 0).replace(',', '')),
                    int(demographics_data.get('hispanicLatino', 0).replace(',', '')),
                    demographics_data.get('americanIndian', 0),
                    demographics_data.get('nativeHawaiian', 0),
                    demographics_data.get('otherRace', 0)
                ]
            }

            racial_df = pd.DataFrame(racial_data)
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x='Race', y='Population', data=racial_df, ax=ax, palette="viridis")
            ax.set_title("Population Distribution by Race")
            st.pyplot(fig)

            # # Pie chart for racial distribution
            # fig2, ax2 = plt.subplots(figsize=(6, 6))
            # ax2.pie(racial_df['Population'], labels=racial_df['Race'], autopct='%1.1f%%', startangle=90, colors=sns.color_palette("viridis", len(racial_df)))
            # ax2.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle.
            # st.pyplot(fig2)    


# Functions to fetch data from Neo4j
def get_context_from_graph(zipcode, feature, uri, auth):
    if feature == "crime":
        return get_crime_context(uri, auth, zipcode)
    elif feature == "restaurants":
        return get_restaurant_context(uri, auth, zipcode)
    elif feature == "parks":
        return get_park_context(uri, auth, zipcode)
    elif feature == "demographics":
        return get_demographics_context(uri, auth, zipcode)
    else:
        return "Feature not recognized. Please ask about crime, restaurants, parks, or demographics."

# Streamlit app UI
def main():
    st.title("Neighborhood Insights")
    st.subheader("Ask me about crime rates, restaurants, parks, or demographics in Fenway, South End, Back Bay, or South Boston!")


    user_input = st.text_input("Enter your question:")
    if st.button("Get Context"):
        if user_input:
            # openai_key = "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"
            uri = "neo4j+ssc://6f4de360.databases.neo4j.io:7687"
            auth = ("neo4j", "yVsGWUmODVg0hAFAioEcWSLdzgFpQAO7k6kD2mjpOoE")
            
            zipcode, feature = parse_user_query(user_input)
            
            if zipcode and feature:
                st.write(f"Fetching {feature} data for {zipcode}...")
                result = get_context_from_graph(zipcode, feature, uri, auth)
                print(result)
                display_data(feature, result)  # Display result as JSON
            else:
                st.error("Couldn't understand your query. Please specify an area and a feature (e.g., 'crime rate in Fenway').")
        else:
            st.warning("Please enter a question.")

if __name__ == "__main__":
    main()
