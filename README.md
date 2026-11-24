# Travel Buddy Agent

A command-line travel-planning agent built with Python, Strands Agents,
a Groq OpenAI-compatible endpoint, Tavily web search, and Open-Meteo weather.

## Files

- `agent.py` - main conversational agent
- `travel_tools.py` - weather, web-search, and budget tools
- `requirements.txt` - Python dependencies
- `.env.example` - template for API keys

## Setup (Windows PowerShell)

Run these commands from this project directory:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Open `.env` and set your own `GROQ_API_KEY` and `TAVILY_API_KEY`.
Do not share the `.env` file or commit it to Git.

Then run:

```powershell
python agent.py
```

If you already have a virtual environment in the parent `strands-project`
folder, you can activate that environment instead of creating another one:

```powershell
..\.venv\Scripts\Activate.ps1
```

## Example prompt

Plan a 3-day trip from Hyderabad to Goa for 2 adults. My total budget is
₹20,000. I like beaches, sightseeing and vegetarian food. Create a
day-by-day itinerary.

## Notes

- Weather is retrieved from Open-Meteo.
- Web research is retrieved through Tavily.
- Budget calculations are local Python calculations.
- Search results and prices should be verified before making bookings.
- This project does not make reservations or purchases.
