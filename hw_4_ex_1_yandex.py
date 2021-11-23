from pprint import pprint
from pymongo import MongoClient
from lxml import html
import requests
from datetime import date
# https://yandex.ru/news/?utm_source=main_stripe_big

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85'
                         ' YaBrowser/21.11.0.1996 Yowser/2.5 Safari/537.36'}
params = {'utm_source': 'main_stripe_big'}
url = 'https://yandex.ru/news/'

responce = requests.get(url, params=params, headers=headers)
dom = html.fromstring(responce.text)

articles = dom.xpath('//article')

news_lsit = []
for article in articles:
    news_dict = {}

    news_dict['source_name'] = ''.join(article.xpath('.//a[@class="mg-card__source-link"]/text()'))
    news_dict['news_title'] =  ''.join(article.xpath('.//a/h2/text()')).replace('\xa0', ' ')# наименование новости;
    news_dict['link'] = ''.join(article.xpath('.//a[@class="mg-card__link"]/@href')) # ссылку на новость;
    news_dict['published'] = str(date.today()) + ' ' + ''.join(article.xpath('.//span[@class="mg-card-source__time"]/text()')) # дата публикации.
    news_lsit.append(news_dict)

client = MongoClient('127.0.0.1', 27017)
db = client['news_2311']
news = db.news

for doc in news_lsit:
    search_res = news.find_one(doc)
    if not search_res:
       news.insert_one(doc)
    else:
       pass

for doc in news.find({}):
    pprint(doc)