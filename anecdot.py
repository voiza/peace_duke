#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

import urllib2
from lxml import html

def get_anecdot():
    response = urllib2.urlopen('https://pda.anekdot.ru/anekdots/random/')
    text = response.read()
    text = text.replace("<br>", "\n")
    tree = html.fromstring(text)
    p = tree.xpath("//p")
    return unicode(p[0].text)

if __name__ == '__main__':
    print(get_anecdot())