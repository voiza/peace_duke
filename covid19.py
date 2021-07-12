#!/usr/bin/python3.7
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
    self.iso2 = json.get('countryInfo')["iso2"]
    self.population = json.get('population')

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

    self.vaccines = None
    self.today_vaccines = None
    self.vaccines_per_1m = None

  def set_vaccines(self, vaccines, today_vaccines, population):
    self.vaccines = vaccines
    self.today_vaccines = today_vaccines
    self.vaccines_per_1m = round(vaccines * 1000000 / population, 2)

  def __repr__(self):
    return "CASES: {0} {1}, DEATHS: {2} {3}".format(
           self.cases, 
           self.today_cases,
           self.deaths,
           self.today_deaths
          )

def get_covid19_today(country=""):
    global cache
    now = datetime.datetime.now()
    if cache.get(TIMESTAMP, datetime.datetime.min) + CACHE_TIME < now:
        url = "https://disease.sh/v3/covid-19/countries/" #+ country
        data_json = requests.get(url).json()
        cache[TIMESTAMP] = now
        for c in data_json:
            cd = CountryData(c)
            cache[c.get(COUNTRY).lower()] = cd

        url = "https://disease.sh/v3/covid-19/vaccine/coverage/countries?lastdays=2"
        vac_json = requests.get(url).json()
        for c in vac_json:
            vac_country = c.get("country")
            vac_country = cache.get(vac_country.lower())
            timeline = list(c.get("timeline").items())
            if vac_country and timeline:
                yesterday, yesterday_vaccines = timeline[0]
                today, vaccines = timeline[1]
                vac_country.set_vaccines(vaccines, vaccines - yesterday_vaccines, vac_country.population)

    country = cache.get(country.lower())
    return (cache[TIMESTAMP], country)
