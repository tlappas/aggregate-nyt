import feedparser
import requests
import datetime
from bs4 import BeautifulSoup
import re
import os

feeds = {
    'home_page':'https://www.nytimes.com/services/xml/rss/nyt/HomePage.xml',
    'world':'https://www.nytimes.com/services/xml/rss/nyt/World.xml',
    'us':'https://www.nytimes.com/services/xml/rss/nyt/US.xml',
    'business':'http://feeds.nytimes.com/nyt/rss/Business',
    'tech':'http://feeds.nytimes.com/nyt/rss/Technology',
    'sports':'https://www.nytimes.com/services/xml/rss/nyt/Sports.xml',
    'sci':'https://www.nytimes.com/services/xml/rss/nyt/Science.xml',
    'health':'https://www.nytimes.com/services/xml/rss/nyt/Health.xml',
    'arts':'https://www.nytimes.com/services/xml/rss/nyt/Arts.xml',
    'travel':'http://rss.nytimes.com/services/xml/rss/nyt/Travel.xml'
}

def save_feeds(path='C:\\Users\\tom.lappas\\code\\aggregate\\data\\raw'):
    date_str = datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d')
    year_month = datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m')
    if os.path.isdir(os.path.join(path, year_month)) == False:
        os.mkdir(os.path.join(path, year_month))
    for rss in feeds.keys():
        resp = requests.get(feeds[rss])
        with open(os.path.join(path, year_month, '{}[{}].xml'.format(date_str, rss)), 'wb') as feed:
            feed.write(resp.text.encode('utf8'))

# def save_current_articles(feed_path):
#     parsed_feed = feedparser.parse(feed_path)
#     for entry in parsed_feed.entries:
#         # This should probably be a regex to limit weird chars
#         title = entry.title.encode('ascii').decode('utf8')
#         # Saving response object for (potential) error handling
#         resp = requests.get(entry.link)
#         text = resp.text

# def delete_old_articles():
#     pass

if __name__ == '__main__':
    save_feeds()
