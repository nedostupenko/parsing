from pprint import pprint
from pymongo import MongoClient
from lxml import html
import requests

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85'
                         ' YaBrowser/21.11.0.1996 Yowser/2.5 Safari/537.36'}

url = 'https://news.mail.ru'

responce = requests.get(url, headers=headers)
dom = html.fromstring(responce.text)

top_news_links = dom.xpath('//div[contains(@class, "daynews__item")]/a/@href')
ordinary_news_links = dom.xpath('//a[@class="list__text"]/@href')
main_news_by_topics_links = dom.xpath('//a[contains(@class, "newsitem__title")]/@href')
news_by_topics_links = dom.xpath('//a[contains(@class, "link link_flex")]/@href')
total_news_links = top_news_links + ordinary_news_links + main_news_by_topics_links + news_by_topics_links

news_lsit = []
for url in total_news_links:
    news_dict = {}

    responce = requests.get(url, headers=headers)
    dom = html.fromstring(responce.text)

    news_dict['source_name'] = ''.join(dom.xpath('//span[@class="note"]/a//text()'))
    news_dict['news_title'] = ''.join(dom.xpath('//span[@class="hdr__text"]/h1/text()')) # наименование новости;
    news_dict['link'] = url # ссылку на новость;
    news_dict['published'] = ''.join(dom.xpath('//span[@class="note"]//@datetime')) # дата публикации.
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