import requests

OPENCAGE_API_KEY = 'd3f582a7f0be4340b0cc7a109b327ae3'
OPENCAGE_API_URL = "https://api.opencagedata.com/geocode/v1/json"

# Function to fetch latitude and longitude using OpenCage API
def get_coordinates(city):
    params = {
        'q': city,
        'key': OPENCAGE_API_KEY,
        'limit': 1
    }
    try:
        response = requests.get(OPENCAGE_API_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            if data['results']:
                location = data['results'][0]['geometry']
                return location['lat'], location['lng']
            else:
                print("No results found for the specified city.")
                return None
        else:
            print("Error with the OpenCage API. Please check the API key or internet connection.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return None
