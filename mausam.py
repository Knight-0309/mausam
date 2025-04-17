import requests
from datetime import datetime, timezone

def convert_unix_to_time(unix_timestamp):
    # Convert Unix timestamp to a timezone-aware UTC datetime
    return datetime.fromtimestamp(unix_timestamp, timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

def get_weather(city_name, api_key):
    # OpenWeatherMap API URL for fetching weather data
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    
    # Construct the full API URL with query parameters (city name, API key, units)
    complete_url = f"{base_url}q={city_name}&appid={api_key}&units=metric"
    
    # Make an HTTP GET request to fetch the weather data
    response = requests.get(complete_url)
    
    # Parse the response as JSON to get the data in Python dictionary format
    data = response.json()

    # Check if the city was found
    if data.get("cod") != 200:
        print(f"Error: {data.get('message', 'Unknown error occurred')} for city: {city_name}")
        return False  # Indicate invalid city
    else:
        # If the city is found, extract weather details from the response
        try:
            main = data["main"]  # Get the 'main' section from the response
            weather = data["weather"][0]  # Get the first weather condition from the list
            wind = data["wind"]  # Get wind data
            clouds = data["clouds"]  # Get cloud coverage data
            sys = data["sys"]  # Get system data (sunrise, sunset, etc.)

            # Extract specific details from the 'main', 'weather', 'wind', 'clouds', and 'sys' sections
            temperature = main["temp"]  # Current temperature in Celsius
            pressure = main["pressure"]  # Atmospheric pressure (hPa)
            humidity = main["humidity"]  # Humidity percentage
            description = weather["description"]  # Weather condition description (e.g., clear sky)
            wind_speed = wind["speed"]  # Wind speed in m/s
            cloudiness = clouds["all"]  # Cloudiness in percentage
            visibility = data["visibility"] / 1000  # Visibility in km (OpenWeatherMap returns in meters)
            sunrise = convert_unix_to_time(sys["sunrise"])  # Convert sunrise from Unix timestamp
            sunset = convert_unix_to_time(sys["sunset"])  # Convert sunset from Unix timestamp

            # Display the extracted weather details
            print(f"\nWeather in {city_name}:")
            print(f"Temperature: {temperature}°C")
            print(f"Pressure: {pressure} hPa")
            print(f"Humidity: {humidity}%")
            print(f"Condition: {description.capitalize()}")
            print(f"Wind Speed: {wind_speed} m/s")
            print(f"Cloudiness: {cloudiness}%")
            print(f"Visibility: {visibility} km")
            print(f"Sunrise: {sunrise}")
            print(f"Sunset: {sunset}")
            return True  # Indicate valid city
        except KeyError:
            print(f"KeyError: Missing expected data for city: {city_name}")
            print(f"Full response: {data}")
            return False  # Indicate some error with data

# Main execution block
if __name__ == "__main__":
    # Your OpenWeatherMap API key here
    api_key = "8503d4490a3c48b33bf360e47cbf6711"  # Replace with your actual API key
    
    while True:  # Infinite loop to keep asking for the city name until valid input
        # Ask the user for the city name
        city_name = input("Enter the name of the city: ")
        
        # Get the weather for the entered city
        valid = get_weather(city_name, api_key)
        
        # If a valid city was entered, ask if the user wants to check another city
        if valid:
            continue_prompt = input("Do you want to check weather for another city? (yes/no): ").strip().lower()
            if continue_prompt != 'yes':
                print("Thank you for using the Weather Information Fetcher. Goodbye!")
                break  # Exit the loop if user does not want to continue
        else:
            print("Please try again with a valid city name.")
