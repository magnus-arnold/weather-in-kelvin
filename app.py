# Copyright (C) 2022, David Arnold

from bottle import Bottle, response, run
import requests

GEO_API = 'https://api.openweathermap.org/data/2.5/weather?q=%s&appid=%s'
API_KEY = 'ceae1539b53e488c4113057e21b04014'

applications = app = Bottle()

f = open('site.js')
JS = f.read()
f.close()

f = open('site.css')
CSS = f.read()
f.close()

f = open('site.html')
HTML = f.read()
f.close()

f = open('search.svg')
SEARCH = f.read()
f.close()


@app.route('/')
def home():
    return HTML


@app.route('/site.js')
def get_js():
    response.set_header('Content-Type', 'text/javascript')
    return JS


@app.route('/site.css')
def get_css():
    response.set_header('Content-type', 'text/css')
    return CSS


@app.route('/search.svg')
def get_search_icon():
    response.set_header('Content-type', 'image/svg+xml')
    return SEARCH


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
    response = requests.get(GEO_API % (place, API_KEY))

    if response.status_code != 200:
        # FIXME: Create a JSON error structure
        print(f"Error: {response.status_code}")
        return

    # Round temperatures to 0.5 K
    data = response.json()
    main = data.get('main')
    if main:
        round_temp(main, "temp")
        round_temp(main, "feels_like")
        round_temp(main, "temp_min")
        round_temp(main, "temp_max")

    return data


if __name__ == "__main__":
    run(app=app, host='localhost', port=8080, debug=True)
