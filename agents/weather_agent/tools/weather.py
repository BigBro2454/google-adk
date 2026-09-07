"""
Weather tools using the Open-Meteo API.

Open-Meteo is a free, open-source weather API — no API key required.
Docs: https://open-meteo.com/en/docs

Two tools:
  1. get_coordinates(city) → lat/lon using the Geocoding API
  2. get_weather(lat, lon)  → current weather using the Forecast API
"""

import urllib.request
import urllib.parse
import json


def get_coordinates(city: str) -> dict:
    """Gets the latitude and longitude for a given city name.

    Always call this first before calling get_weather.
    Uses the Open-Meteo Geocoding API to resolve city names to coordinates.

    Args:
        city: The name of the city to look up (e.g. "Mumbai", "London", "New York").

    Returns:
        A dict with keys:
          - 'latitude' (float): Latitude of the city.
          - 'longitude' (float): Longitude of the city.
          - 'name' (str): Resolved city name.
          - 'country' (str): Country the city is in.
          - 'error' (str): Set only if the city was not found.
    """
    try:
        encoded_city = urllib.parse.quote(city)
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={encoded_city}&count=1&language=en&format=json"

        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())

        if not data.get("results"):
            return {"error": f"City '{city}' not found. Try a different spelling."}

        result = data["results"][0]
        return {
            "latitude": result["latitude"],
            "longitude": result["longitude"],
            "name": result["name"],
            "country": result.get("country", "Unknown"),
        }

    except Exception as e:
        return {"error": f"Failed to get coordinates: {str(e)}"}


def get_weather(latitude: float, longitude: float) -> dict:
    """Gets the current weather for a given latitude and longitude.

    Always call get_coordinates first to get the lat/lon for a city.
    Uses the Open-Meteo Forecast API — free, no API key required.

    Args:
        latitude: Latitude of the location (e.g. 19.07 for Mumbai).
        longitude: Longitude of the location (e.g. 72.87 for Mumbai).

    Returns:
        A dict with current weather data:
          - 'temperature_celsius' (float): Current temperature in Celsius.
          - 'wind_speed_kmh' (float): Wind speed in km/h.
          - 'wind_direction_degrees' (int): Wind direction in degrees.
          - 'weather_condition' (str): Human-readable weather description.
          - 'is_day' (bool): True if it is currently daytime.
          - 'error' (str): Set only if the request failed.
    """
    # WMO Weather Condition Codes → human-readable descriptions
    WMO_CODES = {
        0: "Clear sky",
        1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Foggy", 48: "Icy fog",
        51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
        61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
        71: "Slight snowfall", 73: "Moderate snowfall", 75: "Heavy snowfall",
        77: "Snow grains",
        80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
        85: "Slight snow showers", 86: "Heavy snow showers",
        95: "Thunderstorm", 96: "Thunderstorm with hail", 99: "Thunderstorm with heavy hail",
    }

    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={latitude}&longitude={longitude}"
            f"&current_weather=true"
            f"&temperature_unit=celsius"
            f"&wind_speed_unit=kmh"
        )

        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())

        current = data["current_weather"]
        wmo_code = int(current.get("weathercode", 0))

        return {
            "temperature_celsius": current["temperature"],
            "wind_speed_kmh": current["windspeed"],
            "wind_direction_degrees": current["winddirection"],
            "weather_condition": WMO_CODES.get(wmo_code, f"Unknown (code {wmo_code})"),
            "is_day": bool(current.get("is_day", 1)),
        }

    except Exception as e:
        return {"error": f"Failed to get weather: {str(e)}"}
