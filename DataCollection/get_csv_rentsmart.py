import requests
import pandas as pd
import datetime

# API Endpoint
api_url = 'https://data.boston.gov/api/3/action/datastore_search'

# Start Date
specified_date = '2023-01-01'

# Parameters for API Call
params = {
    'resource_id': 'dc615ff7-2ff3-416a-922b-f0f334f085d0',
    'limit': 32000,  # Maximum
    'offset': 0
}

# Fetch data
def fetch_data(offset):
    params['offset'] = offset
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['success']:
            return data['result']['records'], data['result']['total']
    return None, None

# Fetch all data
all_records = []
total_records = None
offset = 0

while True:
    records, total = fetch_data(offset)
    if records is None:
        print(f"Failed to retrieve data at {offset}")
        break
    
    all_records.extend(records)
    offset += len(records)
    
    if total_records is None:
        total_records = total
    
    print(f"Retrieved {len(all_records)} out of {total_records} records")
    
    if len(all_records) >= total_records:
        break

if all_records:
    df = pd.DataFrame(all_records)
    df['date'] = pd.to_datetime(df['date'])  
    filtered_df = df[df['date'] > specified_date]
    filtered_df.to_csv('rentsmart_data_after_date.csv', index=False)
    print('Data downloaded')
    print(f"Total records after {specified_date}: {len(filtered_df)}")
    print(filtered_df.head())
else:
    print('Failed to retrieve data')
