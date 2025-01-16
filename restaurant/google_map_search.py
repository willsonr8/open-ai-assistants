import googlemaps
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
gmaps = googlemaps.Client(key=os.getenv('GOOGLE_MAPS_API_KEY'))
location = gmaps.geolocate()
all_restaurants = gmaps.places_nearby(location['location'], radius=1000, type='restaurant')  # radius in meters 
# above will also accept keyword arguments like keyword='cruise' or name='Bob's Pizza', open now, min and max price, name


