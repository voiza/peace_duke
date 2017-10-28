#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals

import config
import telebot

import re

import sys
import time

import logging

#logger = telebot.logger
#telebot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.

bot = telebot.TeleBot(config.token)

#https://github.com/eternnoir/pyTelegramBotAPI#methods

@bot.message_handler(content_types=["sticker"]) # content_types["text", "sticker", "pinned_message", "photo", "audio"]
def sticker_handler(message):
    bot.reply_to(message, "pack: %(pack)s\n" \
                          "emoji: %(emoji)s" %  \
                            dict(pack  = message.sticker.set_name, \
                                 emoji = message.sticker.emoji     \
                            ))

@bot.message_handler(content_types=["text"], regexp=config.trigger_regex)
def repeat_all_messages(message):
    bot.reply_to(message, message.text)

sys.tracebacklimit = 0

if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception:
            time.sleep(10)
