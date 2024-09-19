# Weather App

A dynamic and interactive weather application that provides 5-day weather forecasts for cities around the world.

## Features

- Real-time weather data from OpenWeatherMap API
- 5-day weather forecast
- Interactive temperature chart
- Responsive design with animations
- Caching system for improved performance

## Technologies Used

- Backend: Python with Flask
- Frontend: HTML, CSS, JavaScript
- APIs: OpenWeatherMap
- Charts: Chart.js
- HTTP Client: Axios

## Setup and Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/weather-app.git
   cd weather-app
   ```

2. Set up a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory and add your OpenWeatherMap API key:

   ```bash
   OPENWEATHERMAP_API_KEY=your_api_key_here
   ```

5. Run the application:

   ```bash
   python run.py
   ```

6. Open a web browser and navigate to `http://localhost:5000`

## Usage

1. Enter a city name in the input field.
2. Click the "Get Weather" button.
3. View the 5-day forecast and temperature chart.

## API Documentation

API documentation is available at `/api/docs` when the application is running.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).
