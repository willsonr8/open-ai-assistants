from openai import OpenAI
from dotenv import load_dotenv
import os
import googlemaps


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
gmaps = googlemaps.Client(key=os.getenv('GOOGLE_MAPS_API_KEY'))

prompt_dict = {
    1:"You are a personal assistant and your user needs help finding a restaurant that fits within their budget and current preferences." \
        "Use the following list of local restaurants to help them find a place to eat. You will be graded on your performance and possibly" \
        "earn a raise if you do well. You should be prioritizing by restaurant rating and number of reviews.", 
    2: "",
    3: "",
    4: "",
}

def find_restaurants_near_me(keyword=None, min_price=1, max_price=4, name=None, open_now=True, radius=5000):
    location = gmaps.geolocate()
    all_restaurants = gmaps.places_nearby(location['location'], keyword=keyword, min_price=min_price, max_price=max_price, name=name, open_now=open_now, radius=radius, type='restaurant')
    return all_restaurants

def chatbot_find_restaurants_near_me(user_prompt, keyword=None, min_price=1, max_price=4, name=None, open_now=True, miles_radius=5):
    radius = miles_radius * 1609.34  # radius in meters
    restaurants = find_restaurants_near_me(keyword=keyword, min_price=min_price, max_price=max_price, name=name, open_now=open_now, radius=radius)
    prompt = f"{prompt_dict[1]} Here are the restaurants: {restaurants}. Here is more information from the user: {user_prompt}."
    response = client.chat.completions.create(
        model="o1-mini",
        messages=[
            {"role": "user", "content": prompt},
        ]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    # intake prompt or hardcoded options and parse into vars for find_restaurants_near_me
    user_prompt = "I want to eat spicy food but I do not like Indian food. I am thinking that I want thai or spicy wings."
    response = chatbot_find_restaurants_near_me(user_prompt)
    print(response)

    
    