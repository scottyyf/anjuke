#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: test_anjuke.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2021, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""
import json
import os
import sys
import time
from fake_useragent import UserAgent

import requests
from bs4 import BeautifulSoup as bs

from xzl_zu.utils.Zone import ZoneName, AreaDetail

zone_name = ZoneName(
    ['baoan', 'nanshan', 'szlhxq', 'futian', 'longgang', 'luohu', 'buji',
     'guangmingxinqu', 'pingshanxinqu', 'yantian', 'dapengxq',
     'shenzhenzhoubian'],
    ['宝安', '南山', '龙华', '福田', '龙岗', '罗湖', '布吉', '光明', '坪山', '盐田',
     '大鹏新区', '深圳周边'])

session = requests.Session()

headers = {
    'User-Agent': UserAgent().random,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'DNT': '1',
    'Connection': 'keep-alive'
    }

proxy_dict = {
    'http': 'http://192.168.4.178:12333',
    'https': 'http://192.168.4.178:12333'
    }

_param = '?from_area=100&to_area=150'


def get_resp(url):
    # proxy_dict = {'http': '61.135.185.156:80'}
    response = session.get(url, headers=headers)
        # proxies=proxy_dict)
    if not response.ok:
        return False

    if not response.text:
        return False

    return response.text


def test_one_site(site):
    html_content = get_resp(site)

    bs_info = bs(html_content, features='html.parser')
    all_info = bs_info.find_all('div', attrs={'class': 'list-item'})
    for item in all_info:
        url = item.find('a')['href']
        desc = item.find('p', attrs={'class': 'item-descript'})

        _desc = ''.join(x.get_text().replace(' ', '') for x in desc.find_all('span'))
        # x = item.findall('p', attrs={'class': 'item-descript'})
        # x = item.find_all('p', attrs=)
        month_price = item.find('div', attrs={'class': 'price-daily'})
        try:
            _month_price = ''.join(x.get_text() for x in month_price.find_all('span'))
        except AttributeError as e:
            # print(f'{url} have not given month price, currently')
            _month_price = '0'

        area_space = item.find('p', attrs={'class': 'area'})
        _area_space = ''.join(x.get_text() for x in area_space.find_all('span'))
        # print(x)
        print(url, _desc, _month_price, _area_space)


def parse_zone_url():
    ret_content = {}
    if os.path.isfile('anjuke.json'):
        print('Already dump anjuke url to file anjuke.json')
        return

    ret = get_resp('https://sz.sydc.anjuke.com/xzl-zu/')
    if not ret:
        raise ValueError

    bs_info = bs(ret, features='html.parser')
    all_url = bs_info.find_all('div', attrs={'id': "district-item",
                                             'class': "item-content"})
    for a in all_url:
        for d in a.find_all('a'):
            if d['title'].startswith('不限'):
                continue

            # print(d['href'], d['title'])
            ret_content.update(get_mini_zone_url_by_zone(d['href']))
            time.sleep(2)

    if ret_content:
        with open('anjuke.json', 'w', encoding='utf-8') as f:
            json.dump(ret_content, f, ensure_ascii=False, indent=4)


def get_mini_zone_url_by_zone(url):
    content = {}
    ret = get_resp(url)
    if not ret:
        print(f'{url} failed')
        return

    bs_info = bs(ret, features='html.parser')
    all_url = bs_info.find_all(
        'div', attrs={'class': 'filter-items sub-items block-list'})
    for a in all_url:
        for d in a.find_all('a'):
            # if d['title'].startswith('不限'):
            if d['title'].startswith('不限'):
                continue

            # print(d['href'], d['title'])
            print('=' * 20, f' DOWNLOADDING current url is {d["href"]} ',
                  '=' * 20)
            # raise ValueError
            content.setdefault(d['href'], f'{d.get_text()}')

    return content


def parse_subway():
    ret_content = {}
    if os.path.isfile('anjuke_subway.json'):
        print('Already dump anjuke url to file anjuke_subway.json')
        return

    ret = get_resp('https://sz.sydc.anjuke.com/xzl-zu/')
    if not ret:
        raise ValueError

    bs_info = bs(ret, features='html.parser')
    all_url = bs_info.find_all('div', attrs={'id': "subway-item",
                                             'class': "item-content"})
    for a in all_url:
        for d in a.find_all('a'):
            if d.get_text().startswith('不限'):
                continue

            # print(d['href'], d['title'])
            ret_content.update(get_mini_zone_url_by_zone(d['href']))
            time.sleep(2)

    if ret_content:
        with open('anjuke_subway.json', 'w', encoding='utf-8') as f:
            json.dump(ret_content, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    # parse_zone_url()
    # test_one_site('https://sz.sydc.anjuke.com/xzl-zu/dt70/?from_area=150&to_area=200')
    parse_subway()

# 如果没有匹配， 那么会有 “没有结果，请换个”
# 　具体路径尾　https://sz.sydc.anjuke.com/xzl-zu/nanshan-baishizhou-p2/?from_area
# =100&to_area=150
# 如果有next，则往下一个page查询
# 　获取深圳安居客首页，并获取各个区的ref
# 　通过区ｒｅｆ下的各个小区域，得到ｒｅｆ
# 进入小区域，并获取至最后一页的所有房价信息
# 信息包括。主题， 地点（南山，大冲，大冲商务中心） 每月租金 建筑面积 单价（每平每天）
