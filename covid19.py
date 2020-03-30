#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

import datetime
import requests
import itertools

TIMESTAMP = 'TS'
DATA = 'DATA'
COUNTRY = 'country'
cache = {}

class CountryData(object):
  def __init__(self, json={}):
    self.country = json.get('country')
    self.cases = json.get('cases')
    self.today_cases = json.get('todayCases')
    self.deaths = json.get('deaths')
    self.today_deaths = json.get('todayDeaths')
    self.recovered = json.get('recovered')
    self.active_cases = json.get('active')

  def __repr__(self):
    return "CASES: {0} {1}, DEATHS: {2} {3}".format(
           self.cases, 
           self.today_cases,
           self.deaths,
           self.today_deaths
          )

def get_covid19_today(country=""):
    now = datetime.datetime.now()
    if cache.get(TIMESTAMP, datetime.datetime.min) + datetime.timedelta(hours=1) < now:
        url = "https://corona.lmao.ninja/countries/" #+ country
        data_json = requests.get(url).json()
        cache[TIMESTAMP] = now
        for c in data_json:
            cd = CountryData(c)
            cache[c.get(COUNTRY).lower()] = cd

    country = cache.get(country.lower())
    return country
