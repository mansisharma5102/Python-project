from auth import register, login, forgot_password
from location import get_coordinates
from sunrise_sunset import get_sunrise_sunset_data, display_sunset_sunrise_data

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

if __name__ == "__main__":
    main()
