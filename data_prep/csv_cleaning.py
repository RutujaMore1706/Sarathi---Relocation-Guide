import pandas as pd

df = pd.read_csv('Data files/zillow_02218_zip_data.csv')

columns_to_drop = [
    'dateSold', 
    'lotAreaValue', 
    'country', 
    'currency', 
    'lotAreaUnit', 
    'isBuilding', 
    'roomForRent',
    'variableData_type', 
    'variableData_isRead', 
    'variableData_isFresh', 
    'variableData_text', 
    'propertyType',
    'contingentListingType',
    'zestimate',
    'listingSubType',
    'rentZestimate',
    'daysOnZillow'
]
df.drop(columns=columns_to_drop, inplace=True)

# Replace empty values in specific columns with '99'
df['bedrooms'] = df['bedrooms'].replace('', '99')
df['bathrooms'] = df['bathrooms'].replace('', '99')
df['livingArea'] = df['livingArea'].replace('', '99')
# df.fillna(value='None', inplace=True)
# columns_to_replace = ['bedrooms', 'bathrooms', 'livingArea']
# df[columns_to_replace] = df[columns_to_replace].replace({None: '99', '': '99'})

df.to_csv('Data files/02218_cleaned_listings.csv', index=False)

print("Data has been cleaned and saved to '02218_cleaned_listings.csv'")
