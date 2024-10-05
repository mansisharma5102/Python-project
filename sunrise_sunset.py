import requests
from datetime import datetime, timedelta

SUNRISE_SUNSET_API_URL = "https://api.sunrise-sunset.org/json"

# Function to fetch sunrise and sunset data from API using latitude and longitude
def get_sunrise_sunset_data(lat, lng):
    params = {
        'lat': lat,
        'lng': lng,
        'formatted': 0
    }
    try:
        response = requests.get(SUNRISE_SUNSET_API_URL, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print("Error fetching data from the Sunrise-Sunset API.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return None

# Function to convert UTC time to IST
def format_utc_to_ist(utc_time_str, time_format='%H:%M:%S'):
    utc_time = datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%M:%S+00:00")
    ist_time = utc_time + timedelta(hours=5, minutes=30)
    return ist_time.strftime(time_format)

# Function to format day length from seconds to HH:MM:SS
def format_day_length(seconds):
    return str(timedelta(seconds=int(seconds)))

# Function to display sunrise and sunset data in IST
def display_sunset_sunrise_data(api_response_data):
    if api_response_data and api_response_data['status'] == 'OK':
        results = api_response_data['results']
        sunrise_utc = results['sunrise']
        sunset_utc = results['sunset']
        day_length_seconds = results['day_length']
        solar_noon_utc = results['solar_noon']

        sunrise_ist = format_utc_to_ist(sunrise_utc)
        sunset_ist = format_utc_to_ist(sunset_utc)
        solar_noon_ist = format_utc_to_ist(solar_noon_utc)

        formatted_day_length = format_day_length(day_length_seconds)

        print(f"Sunrise Time (IST): {sunrise_ist}")
        print(f"Sunset Time (IST): {sunset_ist}")
        print(f"Day Length: {formatted_day_length}")
        print(f"Solar Noon (IST): {solar_noon_ist}")
    else:
        print("Could not retrieve data. Please try again.")
