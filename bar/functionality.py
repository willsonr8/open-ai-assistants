from openai import OpenAI
from dotenv import load_dotenv
import os
import googlemaps


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
gmaps = googlemaps.Client(key=os.getenv('GOOGLE_MAPS_API_KEY'))

prompt_dict = {
    1:"You are a personal assistant and your user needs help finding a bar that fits within their budget and current preferences." \
        "Use the following list of local bars to help them find a place to eat. You will be graded on your performance and possibly" \
        "earn a raise if you do well. You should be prioritizing by bar rating and number of reviews.", 
    2: "You are a personal assistant and your user needs help finding a bar." \
        "Use the following list of local bars to help them find a place to eat. Avoid repeat suggestions such as the same chain with multiple locations." \
        "Promote style variety in your suggestions. Limit your suggestions to a maximum of 5 places. You should be prioritizing by bar rating and number of reviews.",
    3: "",
    4: "",
}

def get_keyword(user_prompt): 
    prompt = f"You are to tasked with analyzing a text prompt and determining the keyword that the user is looking for. The keyword will likely always be related to types of drinks or bar themes. Your response must be exactly one word and it should be somewhat broad. Here is the prompt: {user_prompt}."
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt},
        ]
    )
    return response.choices[0].message.content

def find_bars_near_me(keyword=None, min_price=1, max_price=4, name=None, open_now=True, radius=5000):
    location = gmaps.geolocate()
    all_bars = gmaps.places_nearby(location['location'], keyword=keyword, min_price=min_price, max_price=max_price, name=name, open_now=open_now, radius=radius, type='bar')
    return all_bars

def chatbot_find_bars_near_me(user_prompt, min_price=1, max_price=4, name=None, open_now=True, miles_radius=5):
    radius = miles_radius * 1609.34  # radius in meters
    keyword = get_keyword(user_prompt)
    print(f"Keyword: {keyword}")
    bars = find_bars_near_me(keyword=keyword, min_price=min_price, max_price=max_price, name=name, open_now=open_now, radius=radius)
    for i in range(len(bars['results'])):
        print(f"{i}. {bars['results'][i]['name']}\n")
    prompt = f"{prompt_dict[2]} Here are the bars: {bars}. Here is more information from the user: {user_prompt}."
    response = client.chat.completions.create(
        model="o1-mini",
        messages=[
            {"role": "user", "content": prompt},
        ]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    # intake prompt or hardcoded options and parse into vars for find_bars_near_me
    user_prompt = "I am looking for lit vibes but want a place to sit"
    response = chatbot_find_bars_near_me(user_prompt)
    print(response)

    
    