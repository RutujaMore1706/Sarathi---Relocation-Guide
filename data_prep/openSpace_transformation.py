import pandas as pd

df = pd.read_csv('boston_openSpace_data.csv')

selected_columns = ['SITE_NAME', 'ACRES', 'TypeLong', 'ZipCode', 'ADDRESS']
df_selected = df[selected_columns]

df_selected = df_selected.dropna(subset=['ZipCode'])
df_selected.to_csv('cleaned_boston_openSpace.csv', index=False)

print("boston_openSpace_selected.csv")