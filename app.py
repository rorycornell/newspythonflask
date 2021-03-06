import feedparser
from flask import Flask, render_template, request
import requests
import json
import urllib2
from bs4 import BeautifulSoup
app = Flask(__name__)




RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
                'cnn': 'http://rss.cnn.com/rss/edition.rss',
                'fox': 'http://feeds.foxnews.com/foxnews/latest',
                'iol': 'http://www.iol.co.za/cmlink/1.640'}



def gethnfrontpage():
    response = urllib2.urlopen("https://news.ycombinator.com/news")
    stories = []
    soup = BeautifulSoup(response, "html.parser")
    posts = soup.select(".storylink")
    for post in posts:
        #title = post.text
        #link = post["href"]
        stories.append({"title":post.text, "link":post["href"]})
    return json.dumps(stories)


#frontpage = gethnfrontpage()
#parsed_json = json.loads(frontpage)
#print(parsed_json[1]['title'])

#for news in parsed_json:
#    print news['title']
#    print news['link']



def get_weather(location):
    payload = {'q':location, 'units':'metric','appid':'cb932829eacb6a0e9ee4f38bfbf112ed'}
    r = requests.get('http://api.openweathermap.org/data/2.5/weather', params=payload)
    parsed_weather_data = json.loads(r.text)
    weather = {"description":parsed_weather_data["weather"][0]["description"],
    "temperature":parsed_weather_data["main"]["temp"],
    "city":parsed_weather_data["name"],
    'country':parsed_weather_data['sys']['country']
    }
    return weather


def getStockPrice(ticker):
    response = urllib2.urlopen('http://www.nasdaq.com/symbol/%s' % ticker)
    soup = BeautifulSoup(response, "html.parser")
    stockprice = soup.find("div", {"id":"qwidget_lastsale"} )
    return stockprice.text


@app.route('/hn')
def get_hn():
    #return gethnfrontpage()
    frontpage = gethnfrontpage()
    #hn = json.loads(frontpage)
    return render_template("hn.html", hn=json.loads(frontpage))

    #frontpage = gethnfrontpage()
    #parsed_json = json.loads(frontpage)
    #print(parsed_json[1]['title'])

    #for news in parsed_json:
    #    print news['title']
    #    print news['link']




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
    stock = request.form.get("ticker")
    if not stock:
        stock = "fonu"
    stockprice = getStockPrice(stock)
    return render_template("home.html", articles=feed['entries'], weather=weather, stockprice=stockprice, stock=stock)
#@app.route("/<publication>")
#def get_news(publication="bbc"):
#    feed=feedparser.parse(RSS_FEEDS[publication])
#    first_article=feed['entries'][0]
#    return render_template("home.html", articles=feed['entries'])



if __name__ == '__main__':
    app.run(port=5000, debug=True)
