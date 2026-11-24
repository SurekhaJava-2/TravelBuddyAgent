import os

import requests
from dotenv import load_dotenv
from strands import tool

load_dotenv()


@tool
def get_weather(city: str, days: int = 5) -> str:
    """Get current weather and forecast for a destination.

    Args:
        city: Destination city name.
        days: Number of forecast days, maximum 16.
    """
    try:
        days = max(1, min(days, 16))

        geo_response = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={
                "name": city,
                "count": 1,
                "language": "en",
                "format": "json",
            },
            timeout=15,
        )
        geo_response.raise_for_status()
        locations = geo_response.json().get("results", [])

        if not locations:
            return f"Could not find location: {city}"

        location = locations[0]

        weather_response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "current": (
                    "temperature_2m,relative_humidity_2m,"
                    "apparent_temperature,precipitation,weather_code"
                ),
                "daily": (
                    "temperature_2m_max,temperature_2m_min,"
                    "precipitation_probability_max"
                ),
                "forecast_days": days,
                "timezone": "auto",
            },
            timeout=20,
        )
        weather_response.raise_for_status()
        data = weather_response.json()

        current = data["current"]
        daily = data["daily"]

        lines = [
            f"Weather report: {city}",
            f"Current temperature: {current['temperature_2m']} °C",
            f"Feels like: {current['apparent_temperature']} °C",
            f"Humidity: {current['relative_humidity_2m']}%",
            f"Precipitation: {current['precipitation']} mm",
            "",
            "Forecast:",
        ]

        for index, date in enumerate(daily["time"]):
            lines.append(
                f"{date}: high {daily['temperature_2m_max'][index]} °C, "
                f"low {daily['temperature_2m_min'][index]} °C, "
                f"rain probability "
                f"{daily['precipitation_probability_max'][index]}%"
            )

        return "\n".join(lines)

    except requests.RequestException as exc:
        return f"Weather service error: {exc}"
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        return f"Could not interpret weather response: {exc}"


@tool
def search_travel_info(query: str) -> str:
    """Search the web for travel information such as hotels,
    flights, attractions, restaurants and transportation.

    Args:
        query: Travel research question.
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return "TAVILY_API_KEY is missing from the .env file."

    try:
        response = requests.post(
            "https://api.tavily.com/search",
            json={
                "api_key": api_key,
                "query": query,
                "search_depth": "basic",
                "max_results": 5,
                "include_answer": True,
            },
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()

        output = [f"Search results for: {query}", ""]

        if data.get("answer"):
            output.extend([f"Summary: {data['answer']}", ""])

        for item in data.get("results", []):
            output.extend(
                [
                    f"Title: {item.get('title', 'Untitled')}",
                    f"Content: {item.get('content', '')}",
                    f"URL: {item.get('url', '')}",
                    "",
                ]
            )

        return "\n".join(output)

    except requests.RequestException as exc:
        return f"Travel search error: {exc}"


@tool
def calculate_trip_budget(
    accommodation: float,
    transport: float,
    food: float,
    activities: float,
    miscellaneous: float,
    travelers: int,
) -> str:
    """Calculate estimated trip expenses in Indian Rupees.

    Args:
        accommodation: Total accommodation expense.
        transport: Total transport expense.
        food: Total food expense.
        activities: Total activities and sightseeing expense.
        miscellaneous: Other expenses.
        travelers: Number of travelers.
    """
    if travelers < 1:
        return "Number of travelers must be at least 1."

    costs = {
        "Accommodation": accommodation,
        "Transport": transport,
        "Food": food,
        "Activities": activities,
        "Miscellaneous": miscellaneous,
    }

    if any(value < 0 for value in costs.values()):
        return "Expenses cannot be negative."

    total = sum(costs.values())
    breakdown = "\n".join(
        f"{name}: ₹{amount:,.2f}" for name, amount in costs.items()
    )

    return (
        "TRAVEL BUDGET SUMMARY\n\n"
        f"{breakdown}\n\n"
        f"Total budget: ₹{total:,.2f}\n"
        f"Travelers: {travelers}\n"
        f"Cost per person: ₹{total / travelers:,.2f}"
    )
