#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

import datetime
import requests

USERAGENT = ""
THROTTLING_TIME = datetime.timedelta(seconds=1)

last_joke = "Приходит как-то человек в ботобар и говорит /joke, а бот ему отвечет: this->joke()"
last_ts = datetime.datetime.min

def get_joke():
    global last_joke
    global last_ts
    now = datetime.datetime.now()
    if last_ts + THROTTLING_TIME < now:
        url = "https://icanhazdadjoke.com/"
        headers = {'User-Agent': USERAGENT,
                   'Accept': 'text/plain'}
        last_joke = requests.get(url, headers=headers).content
        last_ts = now
    return last_joke

if __name__ == '__main__':
    print(get_joke())
