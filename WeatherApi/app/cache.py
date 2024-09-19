import json
from datetime import datetime, timedelta

# In-memory cache
cache = {}

def get_cached_weather(city):
    if city in cache:
        data, timestamp = cache[city]
        if datetime.now() - timestamp < timedelta(hours=12):
            return json.loads(data)
    return None

def set_cached_weather(city, weather_data):
    cache[city] = (json.dumps(weather_data), datetime.now())