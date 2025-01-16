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
    user_prompt = "I want to eat spicy food but I do not like Indian food."
    restaurants = find_restaurants_near_me()
    prompt = f"You are a personal assistant and your user needs help finding a restaurant that fits within their budget and current preferences." \
             f"Use the following list of local restaurants to help them find a place to eat. You will be graded on your performance and possibly" \
            f"earn a raise if you do well. Here are the restaurants: {restaurants}. Here is more information from the user: {user_prompt}"
    
    response = client.chat.completions.create(
        model="o1-mini",
        messages=[
            {"role": "user", "content": prompt},
        ]
    )
    print(response.choices[0].message.content)

    
    