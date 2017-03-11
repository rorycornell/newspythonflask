import urllib2
from bs4 import BeautifulSoup
import json

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


frontpage = gethnfrontpage()
parsed_json = json.loads(frontpage)
print(parsed_json[1]['title'])

for news in parsed_json:
    print news['title']
    print news['link']
