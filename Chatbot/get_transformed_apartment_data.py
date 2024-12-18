import json
import re
# Original JSON data
data = []

def transform_apartment_data(data):
    
    data = re.sub(r'[^\x20-\x7E\n\r\t]', '', data)
    data = json.loads(data)
    converted_data = []

    for entry in data:

        apartment = entry["Apartment"]
        nearby_places = entry["Nearby Places"]
        
        # Format apartment data
        apt_address = apartment["apt_address"]
        apt_bedroom_count = apartment["apt_bedroom_count"]
        apt_bathroom_count = apartment["apt_bathroom_count"]
        apt_latitude = apartment["apt_latitude"]
        apt_longitude = apartment["apt_longitude"]
        apt_rent = int(apartment["apt_rent"].replace("$", "").replace(",", ""))
        apt_living_area = apartment['apt_living_area']
        apt_transit_score = apartment["apt_transit_score Score"]
        apt_url = apartment["apt_url"]
        apt_image_url = apartment["apt_image_url"]
        apt_unit  = apartment["apt_unit"]
        apt_building_name = apartment["apt_building_name"]
        
        # Prepare restaurants list
        restaurants = []
        for restaurant in nearby_places["Restaurants"]:
            restaurants.append({
                "name": restaurant["restaurant_name"],
                "yelp_link": restaurant["restaurant_url"],
                "cuisine": restaurant["restaurant_cuisine"],
                "walking_time": restaurant["walking_time Time"]
            })
        
        # Prepare parks list
        parks = []
        for park in nearby_places["Parks"]:
            parks.append({
                "name": park["openspace_name"],
                "walking_distance": park["walking_time Time"]
            })
        
        # Prepare subway stations list
        subway_stations = []
        for station in nearby_places["Subway Stations"]:
            subway_stations.append({
                "name": station["subway_station_name"],
                "walking_time": station["walking_time"]
            })
        
        # Construct the final data structure
        converted_data.append({
            "apt_address": apt_address,
            "apt_bedroom_count": apt_bedroom_count,
            "apt_bathroom_count": apt_bathroom_count,
            "apt_rent": apt_rent,
            "apt_living_area": apt_living_area,
            "apt_transit_score": apt_transit_score,
            "apt_latitude": apt_latitude,  
            "apt_longitude": apt_longitude,  
            "apt_url": apt_url,
            "apt_image_url": apt_image_url,  
            "apt_zip_code": "02215",  
            "apt_building_name": apt_building_name,  
            "apt_unit": apt_unit,  
            "restaurants": restaurants,
            "parks": parks,
            "subway_stations": subway_stations
        })
    
    return converted_data

#transformed_data = transform_apartment_data(data)

#print(json.dumps(transformed_data, indent=4))


