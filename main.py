#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals

import config
import telebot

import decision
import anecdot

import urllib

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
def repeat_addressed_messages(message):
    bot.reply_to(message, """\
Привет, я {0}! Спроси меня, что-то вроде
"Что мне выбрать, {0}: одно или другое, пятое или десятое"
Я постараюсь помочь с выбором.
{1}
""".format(NAME, FAREWELL))

@bot.message_handler(commands=['anecdot'])
def repeat_addressed_messages(message):
    text = anecdot.get_anecdot()
    if text:
        bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=["text"], regexp=TRIGGER_REGEX)
def repeat_addressed_messages(message):
    question = decision.extract_question(message.text, TRIGGER_REGEX)
    if question:
        answers = decision.split_question(question)
        bot.reply_to(message, decision.decide(answers))

sys.tracebacklimit = 0

if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except urllib.error.HTTPError:
            time.sleep(10)
