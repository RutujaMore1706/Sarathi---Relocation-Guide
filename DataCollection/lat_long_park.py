import pandas as pd
import requests

API_KEY = 'AIzaSyD7x0mOVhfJTX-YYhApKkjz5BNbgVAmwCU'

def get_lat_long(site_name, zip_code):
    try:
        zip_code = 'Boston'
        base_url = 'https://maps.googleapis.com/maps/api/geocode/json'
        params = {
            'address': f'{site_name}, {zip_code}',
            'key': API_KEY
        }
        response = requests.get(base_url, params=params)
        response_data = response.json()

        if response_data['status'] == 'OK':
            location = response_data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
        else:
            print(f"Error fetching data for {site_name}, {zip_code}: {response_data['status']}")
            return None, None
    except Exception as e:
        print(f"Exception occurred: {e}")
        return None, None

df = pd.read_csv('openspace_csv_gold.csv')

df['Latitude'] = None
df['Longitude'] = None

for index, row in df.iterrows():
    site_name = row['SITE_NAME']
    zip_code = row['ZIP_CODE']

    lat, lng = get_lat_long(site_name, zip_code)
    
    df.at[index, 'Latitude'] = lat
    df.at[index, 'Longitude'] = lng

df.to_csv('openspace_latlong.csv', index=False)

print("Latitude and Longitude added to the CSV file.")
