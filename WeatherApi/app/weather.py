import requests
from ipinfo import getHandler
from dotenv import load_dotenv
import os
import logging

from app.cache import get_cached_weather, set_cached_weather

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_location_from_ip(ip_address):
    handler = getHandler(os.getenv('IPINFO_TOKEN'))
    try:
        details = handler.getDetails(ip_address)
        city = details.city if hasattr(details, 'city') else None
        country = details.country if hasattr(details, 'country') else None
        return city, country
    except Exception as e:
        print(f"Error getting location from IP: {e}")
        return None, None

def get_weather(city=None, lat=None, lon=None, ip_address=None, days=1):
    api_key = os.getenv('OPENWEATHERMAP_API_KEY')
    if not api_key:
        logger.error("OpenWeatherMap API key is not set")
        return {'error': 'API key is not set'}

    base_url = "http://api.openweathermap.org/data/2.5/forecast"

    if not (city or (lat and lon)):
        city, _ = get_location_from_ip(ip_address)
        if not city:
            logger.error(f"Unable to determine location from IP: {ip_address}")
            return {'error': 'Unable to determine location'}

    params = {
        'appid': api_key,
        'units': 'metric',
        'cnt': days * 8  # 8 forecasts per day
    }

    if city:
        params['q'] = city
    elif lat and lon:
        params['lat'] = lat
        params['lon'] = lon
    else:
        logger.error("No city or coordinates provided")
        return {'error': 'Unable to determine location'}

    logger.info(f"Sending request to OpenWeatherMap API with params: {params}")
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f"Error fetching weather data: {response.status_code}, Response: {response.text}")
        return {'error': f'Error fetching weather data: {response.status_code}', 'details': response.text}

def get_historical_weather(city, start_date, end_date):
    cache_key = f"{city}_{start_date}_{end_date}"
    cached_data = get_cached_weather(cache_key)
    if cached_data:
        return cached_data

    BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
    API_KEY = os.getenv('VISUALCROSSING_API_KEY')

    if not API_KEY:
        return {'error': 'API key for Visual Crossing Weather API is not set'}

    url = f'{BASE_URL}/{city}/{start_date}/{end_date}?unitGroup=metric&key={API_KEY}&contentType=json'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()
        
        processed_data = {
            'city': city,
            'historical_data': []
        }
        
        for day in weather_data['days']:
            processed_data['historical_data'].append({
                'date': day['datetime'],
                'max_temp': day['tempmax'],
                'min_temp': day['tempmin'],
                'description': day['conditions']
            })
        
        set_cached_weather(cache_key, processed_data)
        return processed_data
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}