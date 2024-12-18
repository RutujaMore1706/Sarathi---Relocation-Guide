import requests

url = "https://bostonopendata-boston.opendata.arcgis.com/api/download/v1/items/2868d370c55d4d458d4ae2224ef8cddd/csv?layers=0"


response = requests.get(url)

if response.status_code == 200:
    with open("boston_openSpace_data.csv", "wb") as file:
        file.write(response.content)
    print("CSV file downloaded successfully.")
else:
    print("Failed to download the CSV file. Status code:", response.status_code)