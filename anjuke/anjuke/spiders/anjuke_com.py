import json
import os
from bs4 import BeautifulSoup as bs
import scrapy
import re
import decimal
from anjuke.items import AnjukeItem


class AnjukeComSpider(scrapy.Spider):
    name = 'anjuke.com'

    allowed_domains = ['sz.sydc.anjuke.com']

    # start_urls = ['https://sz.sydc.anjuke.com/xzl-zu/baoan-baoanlu/?from_area=100&to_area=150']

    @classmethod
    def _load_url_json(cls):
        with open(os.path.join(
                os.path.dirname(os.path.abspath(__file__)), 'anjuke.json'),
                'r',  encoding='UTF-8') as f:
            url_dict = json.load(f)

        return url_dict

    def start_requests(self):
        url_dict = self._load_url_json()
        for url, small_area in url_dict.items():
            yield scrapy.Request(
                url + '?from_area=150&to_area=200',
                meta={'small_area': small_area},
                callback=self.parse)


    def parse(self, response):
        small_area = response.meta['small_area']
        items = []
        bs_info = bs(response.text, 'html.parser')
        all_info = bs_info.find_all('div', attrs={'class': 'list-item'})
        for item in all_info:
            anju_item = AnjukeItem()

            url = item.find('a')['href']

            desc = item.find('p', attrs={'class': 'item-descript'})
            _desc = ''.join(x.get_text().replace(' ', '') for x in desc.find_all('span'))

            month_price = item.find('div', attrs={'class': 'price-daily'})
            try:
                _month_price = ''.join(x.get_text() for x in month_price.find_all('span'))
            except AttributeError:
                continue

            _month_price = re.sub(r'[月租金元/]', '', _month_price)
            if '万' in _month_price:
                _month_price = int(decimal.Decimal(_month_price.replace('万', ''))*10000)
            else:
                _month_price = int(decimal.Decimal(_month_price))

            area_space = item.find('p', attrs={'class': 'area'})
            _area_space = int(decimal.Decimal(
                ''.join(x.get_text().replace(
                    '㎡', '') for x in area_space.find_all('span'))))


            anju_item['location_desc'] = _desc
            anju_item['month_money'] = _month_price
            anju_item['area'] = _area_space
            anju_item['small_area'] = small_area
            anju_item['url'] = url
            items.append(anju_item)

        return items

#     url = scrapy.Field()
#     location_desc = scrapy.Field()
#     month_money = scrapy.Field()
#     area = scrapy.Field()

