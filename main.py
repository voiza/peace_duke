#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals

import config

import telebot
import flag

import isalivethread
import decision
import joke
import covid19

import re
import datetime
import sys
import time

#import logging
#logger = telebot.logger
#telebot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.

TOKEN = config.token
NAME = config.name
TRIGGER_REGEX = config.trigger_regex
FAREWELL = config.farewell

bot = telebot.TeleBot(TOKEN)

#https://github.com/eternnoir/pyTelegramBotAPI#methods

#@bot.message_handler(content_types=["sticker"]) # content_types["text", "sticker", "pinned_message", "photo", "audio"]
#def sticker_handler(message):
#    bot.reply_to(message, "pack: %(pack)s\n" \
#                          "emoji: %(emoji)s" %  \
#                            dict(pack  = message.sticker.set_name, \
#                                 emoji = message.sticker.emoji     \
#                            ))

@bot.message_handler(commands=['start'])
def start(message):
    try:
        bot.reply_to(message, \
"""
Привет, я {0}! Спроси меня, что-то вроде
"Что мне выбрать, {0}: одно или другое, пятое или десятое?"
Я постараюсь помочь с выбором.
{1}
""".format(NAME, FAREWELL))
    except Exception:
#        bot.reply_to(message, "Упс")
        pass

@bot.message_handler(commands=['joke'])
def get_joke(message):
    try:
        text = joke.get_joke()
        if text:
            bot.send_message(message.chat.id, text)
    except Exception:
#        bot.reply_to(message, "Упс")
        pass

@bot.message_handler(commands=['decide'])
def decide(message):
    try:
        choices_only = re.sub(r'^\s*\S*\s*', '', message.text)
        if not choices_only:
            raise(Exception)
        answers = decision.split_question(choices_only+"?")
        bot.reply_to(message, decision.decide(answers))
    except Exception:
        bot.reply_to(message, "Лучше так: /decide одно или другое, пятое или десятое")
        pass

@bot.message_handler(commands=['covid'])
def covid(message):
    try:
        country = re.sub(r'^\s*\S*\s*', '', message.text) or 'ukraine'
        (when, covid_data) = covid19.get_covid19_today(country)
        when = datetime.datetime.fromtimestamp(covid_data.when)
        signed = lambda x: "" if None == x else " (" + ("+", "")[x < 0] + str(x) + ")"
        ret = """
{flag} {country} at {when}
😿 cases: {cases}{today_cases} [{cases_per1m}/1M]
🤒 active: {active_cases}{recovered} [{active_per1m}/1M]
⚰️ deaths: {deaths}{today_deaths} [{deaths_per1m}/1M]
👅 tests: {tests} [{tests_per1m}/1M]
💉 vaccines: {vaccines}{today_vaccines} [{vaccines_per1m}/1M]
""".format(country=country,
           flag=flag.flag(covid_data.iso2),
           when=when.strftime("%Y/%m/%d %H:%M"),
           cases=covid_data.cases, 
           today_cases=signed(covid_data.today_cases),
           active_cases=covid_data.active_cases, 
           active_per1m=covid_data.active_cases_per_1m,
           recovered=signed(-covid_data.recovered),
           deaths=covid_data.deaths,
           today_deaths=signed(covid_data.today_deaths),
           cases_per1m=covid_data.cases_per_1m,
           deaths_per1m=covid_data.deaths_per_1m,
           tests=covid_data.tests,
           tests_per1m=covid_data.tests_per_1m,
           vaccines=covid_data.vaccines,
           today_vaccines=signed(covid_data.today_vaccines),
           vaccines_per1m=covid_data.vaccines_per_1m
          )
        bot.reply_to(message, ret)
    except Exception:
        bot.reply_to(message, "no data for today")
        pass

# Since lib adds @bot_name at the end of the regex, should text handlers go last?
@bot.message_handler(content_types=["text"], regexp=TRIGGER_REGEX)
def question_text(message):
    try:
        question = decision.extract_question(message.text, TRIGGER_REGEX)
        if question:
            answers = decision.split_question(question)
            bot.reply_to(message, decision.decide(answers))
    except Exception:
#        bot.reply_to(message, "Упс")
        pass

sys.tracebacklimit = 0

if __name__ == '__main__':
    covid19.CACHE_TIME = config.covid_cache_time
    joke.USERAGENT = config.joke_useragent
    joke.THROTTLING_TIME = config.joke_throttling_time
    sanity_thread = isalivethread.IsAliveThread(bot)
    sanity_thread.start()
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception: # recover from any error, please
            time.sleep(10)
    sanity_thread.stop = True
    sanity_thread.join()
