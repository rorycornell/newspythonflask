import requests

def get_weather(location):
    payload = {'q':location, 'units':'metric','appid':'cb932829eacb6a0e9ee4f38bfbf112ed'}
    r = requests.get('http://api.openweathermap.org/data/2.5/weather', params=payload)
    print r.json()

get_weather("boston, ma")
