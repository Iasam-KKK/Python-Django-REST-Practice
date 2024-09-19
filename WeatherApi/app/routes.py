from flask import jsonify, request, render_template, current_app
from app import app, limiter
from app.weather import get_weather, get_historical_weather
from flask_swagger_ui import get_swaggerui_blueprint

@app.errorhandler(400)
def bad_request(e):
    current_app.logger.error(f'Bad Request: {str(e)}')
    return jsonify(error=str(e)), 400

@app.errorhandler(500)
def internal_server_error(e):
    current_app.logger.error(f'Server Error: {str(e)}')
    return jsonify(error=str(e)), 500

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/weather')
def weather():
    city = request.args.get('city')
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    days = int(request.args.get('days', 1))
    ip_address = request.remote_addr

    weather_data = get_weather(city=city, lat=lat, lon=lon, ip_address=ip_address, days=days)

    if 'error' in weather_data:
        app.logger.error(f"Weather API error: {weather_data}")
        return jsonify(weather_data), 400

    return jsonify(weather_data)

@app.route('/api/historical')
@limiter.limit("5 per minute")
def historical_weather():
    city = request.args.get('city')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not all([city, start_date, end_date]):
        return jsonify({'error': 'City, start_date, and end_date are required'}), 400
    
    weather_data = get_historical_weather(city, start_date, end_date)
    if 'error' in weather_data:
        return jsonify(weather_data), 500
    
    return jsonify(weather_data)

# Swagger UI
SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Weather API"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)