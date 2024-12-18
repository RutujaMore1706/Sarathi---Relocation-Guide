import pandas as pd

df = pd.read_csv('boston_utilities_data.csv')


df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

df = df[df['InvoiceDate'] >= '2023-01-01']

columns_to_remove = [
    'InvoiceID', 'InvoiceDate', 'AccountNumber', 'StreetAddress',
    'StateName', 'Abbreviation', 'CountryName', 'SiteName',
    'Currency', 'CodeDescription', 'City', 'DepartmentName'
]

df = df.drop(columns=columns_to_remove)

df['_ingest_datetime'] = pd.to_datetime(df['_ingest_datetime']).dt.date

df = df.rename(columns={'_ingest_datetime': 'ingest_date'})

df.to_csv('cleaned_boston_utilities_data.csv', index=False)

print("boston_utilities_data_cleaned.csv")