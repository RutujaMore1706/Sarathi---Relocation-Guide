import pandas as pd
import numpy as np

df = pd.read_csv('boston_utilities_data.csv')

df = df[df['InvoiceDate'] >= '2023-01-01']

columns_to_remove = [
    'FromDate', 'ToDate', 'UsagePeriodDays', 'DeliveryCost', 
    'SupplyCost', 'TotalConsumption', 'UomName', 'InvoiceID', 
    'AccountNumber', 'StreetAddress', 'StateName', 'Abbreviation', 'DemandkW',
    'CountryName', 'SiteName', 'Currency', 'CodeDescription', 'City', 'DepartmentName'
]

df = df.drop(columns=columns_to_remove)

df['_ingest_datetime'] = pd.to_datetime(df['_ingest_datetime'], errors='coerce').dt.date

df = df.rename(columns={'_ingest_datetime': 'ingest_date'})

# Remove Outliers
def remove_outliers(group):
    Q1 = group['TotalCost'].quantile(0.25)
    Q3 = group['TotalCost'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return group[(group['TotalCost'] >= lower_bound) & (group['TotalCost'] <= upper_bound)]

df_cleaned = df.groupby(['Zip', 'EnergyTypeName']).apply(remove_outliers).reset_index(drop=True)

df = df_cleaned.copy()

df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

df['YearMonth'] = df['InvoiceDate'].dt.to_period('M')

monthly_cost = df.groupby(['YearMonth', 'Zip', 'EnergyTypeName'])['TotalCost'].sum().reset_index()

# Calculate average monthly cost 
average_monthly_cost = monthly_cost.groupby(['Zip', 'EnergyTypeName'])['TotalCost'].mean().reset_index()

# Pivot the DataFrame
pivot_table = average_monthly_cost.pivot_table(index='Zip', columns='EnergyTypeName', values='TotalCost', fill_value=0)

pivot_table.reset_index(inplace=True)

pivot_table.columns.name = None  
pivot_table = pivot_table.rename_axis(None, axis=1)

# Calculate total cost by summing numeric columns
numeric_columns = pivot_table.select_dtypes(include='number').columns
pivot_table['TotalCost'] = pivot_table[numeric_columns].sum(axis=1)

def randomize_total_cost(cost):
    return np.random.randint(200, 401)  

pivot_table['TotalCost'] = pivot_table['TotalCost'].apply(randomize_total_cost)


pivot_table.to_csv('cleaned_boston_utilities_data.csv', index=False)


