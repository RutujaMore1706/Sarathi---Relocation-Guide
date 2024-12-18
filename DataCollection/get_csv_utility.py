import requests

# URL of the CSV file
url = 'https://data.boston.gov/dataset/city-of-boston-utility-data/resource/35fad26c-1400-46b0-846c-3bb6ca8f74d0/download'

# Sending a GET request to the URL
response = requests.get(url)

# Writing the content to a CSV file
with open('boston_utilities_data.csv', 'wb') as file:
    file.write(response.content)

print('CSV file downloaded successfully.')