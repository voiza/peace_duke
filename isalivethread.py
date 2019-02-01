# -*- coding: utf-8 -*-

import threading
import time

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
            except Exception:
                print("killer is killed")
                time.sleep(self.sleep_time)
                continue

            try:
                ret = self.telebot.get_me()
            except Exception:
                self.kill_bot()

            killer.cancel()
            time.sleep(self.sleep_time)

    def kill_bot(self):
        print("killing")
        self.telebot.stop_polling()
