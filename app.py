import feedparser
from flask import Flask, render_template, request
import requests
import json
app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
                'cnn': 'http://rss.cnn.com/rss/edition.rss',
                'fox': 'http://feeds.foxnews.com/foxnews/latest',
                'iol': 'http://www.iol.co.za/cmlink/1.640'}



def get_weather(location):
    payload = {'q':location, 'units':'metric','appid':'cb932829eacb6a0e9ee4f38bfbf112ed'}
    r = requests.get('http://api.openweathermap.org/data/2.5/weather', params=payload)
    parsed_weather_data = json.loads(r.text)
    weather = {"description":parsed_weather_data["weather"][0]["description"],
    "temperature":parsed_weather_data["main"]["temp"],
    "city":parsed_weather_data["name"]
    }
    return weather



@app.route("/", methods=['GET', 'POST'])
def get_news():
    query = request.form.get("publication")
    if not query or query.lower() not in RSS_FEEDS:
        publication = "bbc"
    else:
        publication = query.lower()
    feed=feedparser.parse(RSS_FEEDS[publication])
    city = request.form.get("city")
    if not city:
        city = "Boston,Ma"
    weather = get_weather(city)
    return render_template("home.html", articles=feed['entries'], weather=weather)
#@app.route("/<publication>")
#def get_news(publication="bbc"): 
#    feed=feedparser.parse(RSS_FEEDS[publication])
#    first_article=feed['entries'][0]
#    return render_template("home.html", articles=feed['entries'])



if __name__ == '__main__':
    app.run(port=5000, debug=True)
