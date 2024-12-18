import requests
import pandas as pd

# Define the URL and headers
# url = "https://api.yelp.com/v3/businesses/search?location=Fenway&sort_by=best_match&limit=50"
# url = "https://api.yelp.com/v3/businesses/search?location=Boston&term=restaurants&radius=5000&categories=mexican&sort_by=best_match&limit=50"
# url = "https://api.yelp.com/v3/businesses/search?location=Boston%2002115&term=indian%20food&radius=10000&categories=indian%20&sort_by=best_match&limit=50"
# url = "https://api.yelp.com/v3/businesses/search?location=Boston%2002115&term=korean%20food&radius=10000&categories=korean&sort_by=best_match&limit=50"
url = "https://api.yelp.com/v3/businesses/search?location=Boston%2002115&term=cvs&radius=10000&categories=medical&sort_by=best_match&limit=50"


headers = {
    "Authorization": "Bearer Am2ZNBgCMJi-dnAVhq6p2ifkZ724dRvggLqNyLFFaT06uCKPRQoS46Br41DJkBafBfFHqjCAM4NvvNq_Mcj-JsIEAYMYYsu3Y3fBLEp55t38p27iu-DJHiCotD__ZnYx"
}

# Perform the GET request
try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raises HTTPError for bad requests (4XX or 5XX)
    data = response.json()  # Parse the JSON response

    # Convert to DataFrame
    businesses = data["businesses"]
    df = pd.DataFrame(businesses)

    # Save to CSV
    df.to_csv("yelp_data_cvs.csv", index=False)
    print("Data saved to 'yelp_data.csv' successfully.")

except requests.exceptions.HTTPError as errh:
    print("HTTP Error:", errh)
except requests.exceptions.ConnectionError as errc:
    print("Error Connecting:", errc)
except requests.exceptions.Timeout as errt:
    print("Timeout Error:", errt)
except requests.exceptions.RequestException as err:
    print("OOps: Something Else", err)
except KeyError:
    print("Error: JSON response does not have the expected key 'businesses'")
except Exception as e:
    print("An unexpected error occurred:", e)
