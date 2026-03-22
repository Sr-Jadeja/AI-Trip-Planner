import os
import requests
from typing import List
from dotenv import load_dotenv
from langchain.tools import tool
from langchain_tavily import TavilySearch
from langchain_google_community import GooglePlacesTool, GooglePlacesAPIWrapper

load_dotenv()


# ── Weather Tools ──────────────────────────────────────────────

@tool
def get_current_weather(city: str) -> str:
    """Get current weather for a city"""
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather"
    res = requests.get(url, params={"q": city, "appid": api_key, "units": "metric"})
    if res.status_code == 200:
        data = res.json()
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        return f"Current weather in {city}: {temp}°C, {desc}"
    return f"Could not fetch weather for {city}"


@tool
def get_weather_forecast(city: str) -> str:
    """Get weather forecast for a city"""
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/forecast"
    res = requests.get(url, params={"q": city, "appid": api_key, "cnt": 10, "units": "metric"})
    if res.status_code == 200 and "list" in res.json():
        items = res.json()["list"]
        lines = [f"{i['dt_txt'].split()[0]}: {i['main']['temp']}°C, {i['weather'][0]['description']}" for i in items]
        return f"Forecast for {city}:\n" + "\n".join(lines)
    return f"Could not fetch forecast for {city}"


# ── Place Search Tools ─────────────────────────────────────────

def _google_search(query: str) -> str:
    """Helper: search Google Places, fallback to Tavily"""
    try:
        wrapper = GooglePlacesAPIWrapper(gplaces_api_key=os.getenv("GPLACES_API_KEY"))
        return GooglePlacesTool(api_wrapper=wrapper).run(query)
    except Exception:
        tavily = TavilySearch(topic="general", include_answer="advanced")
        result = tavily.invoke({"query": query})
        return result.get("answer", str(result)) if isinstance(result, dict) else str(result)


@tool
def search_attractions(place: str) -> str:
    """Search top attractions of a place"""
    return _google_search(f"top attractions in {place}")


@tool
def search_restaurants(place: str) -> str:
    """Search top restaurants in a place"""
    return _google_search(f"top 10 restaurants in {place}")


@tool
def search_activities(place: str) -> str:
    """Search activities available in a place"""
    return _google_search(f"activities in and around {place}")


@tool
def search_transportation(place: str) -> str:
    """Search transportation options in a place"""
    return _google_search(f"modes of transportation available in {place}")


# ── Expense / Calculator Tools ─────────────────────────────────

@tool
def estimate_hotel_cost(price_per_night: float, total_days: float) -> float:
    """Calculate total hotel cost given nightly rate and number of days"""
    return price_per_night * total_days


@tool
def calculate_total_expense(costs: List[float]) -> float:
    """Calculate total trip expense from a list of costs"""
    return sum(costs)


@tool
def calculate_daily_budget(total_cost: float, days: int) -> float:
    """Calculate average daily budget from total cost and number of days"""
    return total_cost / days if days > 0 else 0


# ── Currency Tool ──────────────────────────────────────────────

@tool
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """Convert amount from one currency to another"""
    api_key = os.getenv("EXCHANGE_RATE_API_KEY")
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{from_currency}"
    res = requests.get(url)
    if res.status_code != 200:
        return "Currency API call failed"
    rates = res.json().get("conversion_rates", {})
    if to_currency not in rates:
        return f"{to_currency} not found in exchange rates"
    converted = amount * rates[to_currency]
    return f"{amount} {from_currency} = {converted:.2f} {to_currency}"


# ── All tools list ─────────────────────────────────────────────

ALL_TOOLS = [
    get_current_weather,
    get_weather_forecast,
    search_attractions,
    search_restaurants,
    search_activities,
    search_transportation,
    estimate_hotel_cost,
    calculate_total_expense,
    calculate_daily_budget,
    convert_currency,
]
