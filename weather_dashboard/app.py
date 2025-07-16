from flask import Flask, render_template, request
import requests

app = Flask(__name__)


def get_coordinates(city):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city, "count": 1}
    r = requests.get(url, params=params)
    data = r.json()
    results = data.get("results")
    if results:
        return results[0]["latitude"], results[0]["longitude"]
    return None, None


def get_weather(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True
    }
    r = requests.get(url, params=params)
    data = r.json()
    return data.get("current_weather")


@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    city = None
    if request.method == 'POST':
        city = request.form.get('city')
        lat, lon = get_coordinates(city)
        if lat and lon:
            weather = get_weather(lat, lon)
    return render_template('index.html', weather=weather, city=city)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
