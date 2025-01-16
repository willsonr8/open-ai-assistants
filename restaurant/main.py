from openai import OpenAI
from dotenv import load_dotenv
import os
import googlemaps

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
gmaps = googlemaps.Client(key=os.getenv('GOOGLE_MAPS_API_KEY'))

def find_restaurants_near_me(keyword=None, min_price=1, max_price=4, name=None, open_now=True, radius=1000):
    location = gmaps.geolocate()
    all_restaurants = gmaps.places_nearby(location['location'], keyword=keyword, min_price=min_price, max_price=max_price, name=name, open_now=open_now, radius=radius, type='restaurant')
    return all_restaurants

if __name__ == "__main__":
    # intake prompt or hardcoded options and parse into vars for find_restaurants_near_me
    print(find_restaurants_near_me())

    assistant = client.beta.assistants.create(
    name="Restaurant Assistant",
    instructions="""You are a personal assistant who's job it is to pick a restaurant that best aligns with the requirements
    given tou you. Use the find_restaurants_near_me function to generate a list of restaurants nearby and determine which one is most suitable for your employer to eat at.""",
    tools=[{
        "type": "function", 
        "function": {
            "name": "find_restaurants_near_me", 
            "description":"This function will return a list of restaurants near you."}}],
    model="gpt-4o-mini",
    )

    thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Where can I get dinner tonight? I am in the mood for something spicy.",
    )
    