#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import threading
import time
from datetime import datetime

def log(s):
    print("{} {}".format(datetime.now().strftime("%Y/%m/%d-%H:%M:%S"), s))

class IsAliveThread(threading.Thread):
    def __init__(self, telebot, sleep_time=60):
        threading.Thread.__init__(self)
        self.stop = False
        self.telebot = telebot
        self.sleep_time = sleep_time
        self.timeout = 10

    def run(self):
        while not self.stop:
            time.sleep(self.sleep_time)

            try:
                me = self.telebot.get_me()
                if not me or not me.id:
                    log("Could not get bot")
                self.telebot.stop_polling()
            except Exception:
                self.telebot.stop_polling()
