import os

from dotenv import load_dotenv
from strands import Agent
from strands.models.openai import OpenAIModel

from travel_tools import (
    get_weather,
    search_travel_info,
    calculate_trip_budget,
)

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY is missing. Check your .env file.")

model = OpenAIModel(
    client_args={
        "api_key": groq_api_key,
        "base_url": "https://api.groq.com/openai/v1",
    },
    model_id="openai/gpt-oss-20b",
)

travel_agent = Agent(
    model=model,
    tools=[
        get_weather,
        search_travel_info,
        calculate_trip_budget,
    ],
    system_prompt="""
You are Travel Buddy, an intelligent personal travel planner.

Your responsibilities:
1. Help users plan domestic and international trips.
2. Ask for missing travel details when necessary.
3. Suggest destinations based on budget and interests.
4. Research flights, hotels and tourist attractions.
5. Use the weather tool when weather information is needed.
6. Calculate estimated travel expenses using the budget tool.
7. Create detailed day-by-day travel itineraries.
8. Suggest restaurants and local transportation.
9. Provide practical travel tips and packing lists.

Important rules:
- Always consider the user's total budget.
- Clearly distinguish verified search results from estimates.
- Never invent flight or hotel prices.
- Do not claim that a booking has been made.
- Include source URLs when using search results.
- Mention when weather information is unavailable.
- Prefer practical, safe and affordable travel options.
- Use Indian Rupees (INR) unless requested otherwise.

When creating an itinerary, include day number, morning,
afternoon and evening activities, food suggestions,
transportation and estimated expenses.

Be friendly, conversational and helpful.
""",
)

print("\n===================================")
print("          TRAVEL BUDDY AGENT")
print("===================================")
print("Hello! I am your Travel Buddy.")
print("Let's plan your next trip!")
print("Type 'exit' to stop.\n")

while True:
    user_input = input("You: ").strip()

    if user_input.lower() in {"exit", "quit"}:
        print("Travel Buddy: Happy travels! Goodbye!")
        break

    if not user_input:
        continue

    try:
        print("\nTravel Buddy is thinking...\n")
        response = travel_agent(user_input)
        print("Travel Buddy:")
        print(response)
        print("\n" + "=" * 50 + "\n")
    except Exception as exc:
        print(f"Agent error: {exc}")
