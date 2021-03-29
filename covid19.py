#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

import datetime
import requests
import itertools

CACHE_TIME = datetime.timedelta(hours=1)
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

    self.cases_per_1m = json.get('casesPerOneMillion')
    self.deaths_per_1m = json.get('deathsPerOneMillion')
    self.active_cases_per_1m = json.get('activePerOneMillion')

    self.tests = json.get('tests')
    self.tests_per_1m = json.get('testsPerOneMillion')
    self.when = json.get('updated')/1000

  def __repr__(self):
    return "CASES: {0} {1}, DEATHS: {2} {3}".format(
           self.cases, 
           self.today_cases,
           self.deaths,
           self.today_deaths
          )

def get_covid19_today(country=""):
    now = datetime.datetime.now()
    if cache.get(TIMESTAMP, datetime.datetime.min) + CACHE_TIME < now:
        url = "https://disease.sh/v3/covid-19/countries/" #+ country
        data_json = requests.get(url).json()
        cache[TIMESTAMP] = now
        for c in data_json:
            cd = CountryData(c)
            cache[c.get(COUNTRY).lower()] = cd

    country = cache.get(country.lower())
    return (cache[TIMESTAMP], country)
