# Copyright (C) 2022, David Arnold

from bottle import Bottle, response, run, static_file
import requests


GEO_API = 'https://api.openweathermap.org/data/2.5/weather?q=%s&appid=%s'
API_KEY = 'ceae1539b53e488c4113057e21b04014'

application = app = Bottle()


@app.route('/')
def home():
    return static_file('site.html', '')


@app.route('/site.js')
def get_js():
    return static_file('site.js', '')


@app.route('/site.css')
def get_css():
    return static_file('site.css', '')


@app.route('/search.svg')
def get_search_icon():
    return static_file('search.svg', '')


def round_temp(container: dict, name: str):
    value = container.get(name)
    if value is not None:
        fraction = value % 1
        if fraction < 0.25:
            result = int(value)
        elif fraction < 0.75:
            result = int(value) + 0.5
        else:
            result = int(value) + 1
        container[name] = result
    return


@app.route('/weather/<place>')
def get_weather(place: str):

    # Try to find weather for the supplied place.
    weather = requests.get(GEO_API % (place, API_KEY))

    if weather.status_code != 200:
        print(f'ERROR: status {weather.status_code} fetching data for "{place}"')
        response.status = weather.status_code
        return

    # Round temperatures to 0.5 K
    data = weather.json()
    main = data.get('main')
    if main:
        round_temp(main, "temp")
        round_temp(main, "feels_like")
        round_temp(main, "temp_min")
        round_temp(main, "temp_max")

    return data


if __name__ == "__main__":
    run(app=app, host='localhost', port=8080, debug=True)
