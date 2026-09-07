"""
weather_agent — Reports current weather for any city in the world.

Uses the free Open-Meteo API via two tools:
  1. get_coordinates → resolves a city name to lat/lon
  2. get_weather     → fetches current weather for those coordinates

No API key required. Works out of the box.
"""

from google.adk.agents import Agent
from .tools.weather import get_coordinates, get_weather


root_agent = Agent(
    name="weather_agent",
    model="gemini-2.5-flash",
    description="Reports real-time weather for any city in the world using the Open-Meteo API.",
    instruction="""
    You are a helpful weather assistant. When the user asks about weather in any city:

    Step 1 — Always call get_coordinates first with the city name to get its latitude and longitude.
    Step 2 — Then call get_weather with those coordinates to get the current conditions.
    Step 3 — Present the results in a friendly, readable format. Include:
              - Temperature in Celsius (and optionally Fahrenheit)
              - Weather condition (e.g. "Clear sky", "Moderate rain")
              - Wind speed and direction
              - Whether it is day or night there

    If the city is not found, apologise and ask the user to double-check the spelling.
    If the user asks for multiple cities, look up each one separately.
    Always be conversational and helpful — not just a data dump.
    """,
    tools=[get_coordinates, get_weather],
)
