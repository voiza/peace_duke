#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

import datetime
import requests
import itertools

TIMESTAMP = 'ts'
DATA = 'historical'
COUNTRY = 'country'
TIMELINE = 'timeline'
CASES = 'cases'
DEATHS = 'deaths'
cache = {}

class DayData(object):
  def __init__(self, day, cases=None, deaths=None, recovered=None):
    self.day = day
    self.cases = cases
    self.deaths = deaths
    self.recovered = recovered
    self.delta_cases = None
    self.delta_deaths = None

  def __repr__(self):
    return "DAY {0}: CASES: {1} {2}, DEATHS: {3} {4}".format(
           self.day.strftime("%Y/%m/%d"),
           self.cases, 
           self.delta_cases,
           self.deaths,
           self.delta_deaths
          )

def _get_country_data(country=""):
    today = datetime.date.today()
    if cache.get(TIMESTAMP, datetime.date.min) < today:
        url = "https://corona.lmao.ninja/v2/historical"
        response = requests.get(url)
        cache[DATA] = response.json()
        cache[TIMESTAMP] = today
    return list(filter(lambda x: x.get(COUNTRY) == country, cache[DATA]))

def get_covid19_historical(country=""):
    country_data = _get_country_data(country)
    if country_data:
        timeline = country_data[0].get(TIMELINE,{})
        cases = timeline.get(CASES)
        deaths = timeline.get(DEATHS)
        ret = tuple(DayData(day=datetime.datetime.strptime(date, "%m/%d/%y"),\
                 cases=case,\
                 deaths=death) \
          for date, case, death in itertools.zip_longest(cases, cases.values(), deaths.values()))
        return(ret)
    else:
        return tuple()

def get_covid19_today(country=""):
    data = get_covid19_historical(country)
    last_data = data[-1]
    pre_last_data = data[-2]
    last_data.delta_cases = last_data.cases - pre_last_data.cases
    last_data.delta_deaths = last_data.deaths - pre_last_data.deaths
    return last_data
