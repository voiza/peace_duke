#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals

import config
import telebot
import isalivethread

import decision
import anecdot
import covid19

import re

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

@bot.message_handler(commands=['anecdot'])
def anecdot(message):
    try:
        text = anecdot.get_anecdot()
        if text:
            bot.send_message(message.chat.id, text)
    except Exception:
#        bot.reply_to(message, "Упс")
        pass

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
        covid_data = covid19.get_covid19_today('ukraine')
        signed = lambda x: "" if None == x else " (" + ("+", "-")[x < 0] + str(x) + ")"
        ret = """
В Украине на {0}:
заразилось: {1}{2}
умерло: {3}{4}
""".format(covid_data.day.strftime("%Y/%m/%d"),
           covid_data.cases, 
           signed(covid_data.delta_cases),
           covid_data.deaths,
           signed(covid_data.delta_deaths)
          )
        bot.reply_to(message, ret)
    except Exception:
        bot.reply_to(message, "Нет данных на сегодня")
        pass

sys.tracebacklimit = 0

if __name__ == '__main__':
    sanity_thread = isalivethread.IsAliveThread(bot)
    sanity_thread.start()
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception: # recover from any error, please
            time.sleep(10)
    sanity_thread.stop = True
    sanity_thread.join()
