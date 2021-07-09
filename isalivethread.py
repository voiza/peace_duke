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
            try:
                killer = threading.Timer(self.timeout, self.kill_bot)
                killer.start()
                log("killer started")
            except Exception as e:
                log("killer could not start: {}".format(e))
                time.sleep(self.sleep_time)
                continue

            try:
                me = self.telebot.get_me()
                if not me or not me.id:
                    self.kill_bot()
#                log(f"{me}")
            except Exception:
                self.kill_bot()

            killer.cancel()
            time.sleep(self.sleep_time)
            log("killer stopped")

    def kill_bot(self):
        log("killing")
        self.telebot.stop_polling()
