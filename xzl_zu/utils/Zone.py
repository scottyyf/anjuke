#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: Zone.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2021, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""


class ZoneName(object):
    def __init__(self, zone_list, zone_cn_name_list):
        self.zone = zone_list
        self.zone_cn_name = zone_cn_name_list


class AreaDetail(object):
    def __init__(self, area, zone: list, zone_ch_name: list):
        self.area = area
        self.zone = zone
        self.zone_ch_name = zone_ch_name