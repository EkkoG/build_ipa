#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 ciel <ciel@cieldeMBP>
#
# Distributed under terms of the MIT license.

"""
Dingtalk bot
"""

import requests
from optparse import OptionParser

def sendMessage(message, tokens):
    para = {"msgtype": "text", "text": {"content": message},"at": {"atMobiles":[]}}

    for token in tokens:
        url = "https://oapi.dingtalk.com/robot/send?access_token={}".format(token)
        r = requests.post(url, json=para)