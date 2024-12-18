import pandas as pd
import re

df = pd.read_csv('rentsmart_data_after_date.csv')

columns_to_keep = ['date', 'violation_type', 'description', 'address', 'neighborhood', 'zip_code', 'property_type', 'latitude', 'longitude']
df = df[columns_to_keep]

df['address'] = df['address'].apply(lambda x: re.sub(r',\s*\d{5}$', '', x))

df['date'] = pd.to_datetime(df['date']).dt.date

df.to_csv('cleaned_rentsmart_data.csv', index=False)

print("cleaned_rentsmart_data.csv")