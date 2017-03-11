import urllib2
from bs4 import BeautifulSoup

def getstockprice(ticker):
    response = urllib2.urlopen('http://www.nasdaq.com/symbol/%s' % ticker)
    soup = BeautifulSoup(response, "html.parser")
    stockprice = soup.find("div", {"id":"qwidget_lastsale"} )
    print ("The last trade price of %s is " + stockprice.text) % ticker


getstockprice("fonu")
