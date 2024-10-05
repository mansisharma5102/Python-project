import csv
import bcrypt
import re
from datetime import datetime, timedelta
import requests

# CSV file to store user credentials
CSV_FILE = 'regno.csv'

# OpenCage API Key for converting city to latitude and longitude
OPENCAGE_API_KEY = 'd3f582a7f0be4340b0cc7a109b327ae3'

# API URL for Sunrise-Sunset times
SUNRISE_SUNSET_API_URL = "https://api.sunrise-sunset.org/json"

# OpenCage API URL
OPENCAGE_API_URL = "https://api.opencagedata.com/geocode/v1/json"

# Function to register a new user
def register():
    email = input("Enter your email: ")
    
    # Validate email format
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        print("Invalid email format.")
        return
    
    password = input("Enter your password: ")
    
    # Validate password format
    if not validate_password(password):
        print("Password must be at least 8 characters long, contain an uppercase letter, lowercase letter, a digit, and a special character.")
        return

    security_question = input("Enter a security question (e.g., Your pet's name): ")
    security_answer = input("Answer to the security question: ")

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([email, hashed_password, security_question, security_answer])

    print("Registration successful!")

# Function to validate password strength
def validate_password(password):
    if (len(password) < 8 or
        not re.search(r"[A-Z]", password) or
        not re.search(r"[a-z]", password) or
        not re.search(r"\d", password) or
        not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)):
        return False
    return True

# Function to log in a user
def login():
    attempts = 0
    while attempts < 5:
        email = input("Enter your email: ")
        password = input("Enter your password: ")

        with open(CSV_FILE, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                stored_email, stored_hashed_password, _, _ = row
                if email == stored_email and bcrypt.checkpw(password.encode(), stored_hashed_password.encode()):
                    print("Login successful!")
                    return True
        
        attempts += 1
        print(f"Invalid credentials. {5 - attempts} attempts remaining.")

    print("Too many failed attempts. Try again later.")
    return False

# Function to handle forgotten passwords
def forgot_password():
    email = input("Enter your registered email: ")

    with open(CSV_FILE, mode='r') as file:
        rows = list(csv.reader(file))
        for row in rows:
            stored_email, _, security_question, security_answer = row
            if email == stored_email:
                print(f"Security Question: {security_question}")
                answer = input("Your answer: ")
                if answer == security_answer:
                    new_password = input("Enter a new password: ")
                    if not validate_password(new_password):
                        print("Password does not meet security requirements.")
                        return

                    new_hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
                    row[1] = new_hashed_password

                    # Update the CSV with the new password
                    with open(CSV_FILE, mode='w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerows(rows)

                    print("Password reset successful!")
                    return
                else:
                    print("Incorrect security answer.")
                    return
    print("Email not found.")

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

# Function to convert UTC time to IST (Indian Standard Time)
def format_utc_to_ist(utc_time_str, time_format='%H:%M:%S'):
    # Convert the string to a datetime object in UTC
    utc_time = datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%M:%S+00:00")
    
    # Add 5 hours and 30 minutes to convert to Indian Standard Time (IST)
    ist_time = utc_time + timedelta(hours=5, minutes=30)
    
    # Return the time in the desired format (24-hour format)
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

        # Convert UTC times to IST
        sunrise_ist = format_utc_to_ist(sunrise_utc)
        sunset_ist = format_utc_to_ist(sunset_utc)
        solar_noon_ist = format_utc_to_ist(solar_noon_utc)

        # Format day length from seconds
        formatted_day_length = format_day_length(day_length_seconds)

        # Display the formatted results
        print(f"Sunrise Time (IST): {sunrise_ist}")
        print(f"Sunset Time (IST): {sunset_ist}")
        print(f"Day Length: {formatted_day_length}")
        print(f"Solar Noon (IST): {solar_noon_ist}")
    else:
        print("Could not retrieve data. Please try again.")

# Main function to run the console application
def main():
    while True:
        print("\n--- Welcome to the Sunset and Sunrise Times Application ---")
        print("1. Register")
        print("2. Login")
        print("3. Forgot Password")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            register()
        elif choice == '2':
            if login():
                city = input("Enter the city to get sunrise and sunset times: ")
                coordinates = get_coordinates(city)
                if coordinates:
                    lat, lng = coordinates
                    api_response = get_sunrise_sunset_data(lat, lng)
                    display_sunset_sunrise_data(api_response)
        elif choice == '3':
            forgot_password()
        elif choice == '4':
            print("Exiting the application.")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "_main_":
    main()
    