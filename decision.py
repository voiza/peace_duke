#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals

import random
import re

def decide(choices):
    if len(choices) == 1:
        return "Да" if random.randint(0,1) == 1 else "Нет"
    return random.choice(choices)

def extract_question(raw_string, refer_to_regex):
    if not re.match("\\\\?", raw_string):
        raise Exception("Not a question")

    pre_variation_regex=".*"+refer_to_regex+".*(:|-)\\s?";
    pre_rc = re.compile(pre_variation_regex)
    if pre_rc.search(raw_string):
        return pre_rc.sub("", raw_string)

    post_variation_regex="[?.,][^,^.^?]*"+refer_to_regex+".*\\?"
    post_rc = re.compile(post_variation_regex)
    if post_rc.search(raw_string):
        return post_rc.sub("?", raw_string)

def split_question(question_str):
    p = re.split("\\s?(?:,|или|or)\\s?", question_str[:-1])
    return set(p)

if __name__ == '__main__':
    import sys
    #in_str = raw_input("Enter a question: ")
    data = [ {'r': "Пездюк, что лучше - вилкой в глаз или в топку всё?"
             ,'q': "вилкой в глаз или в топку всё?"
             ,'s': set(["вилкой в глаз", "в топку всё"])}
           , {'r': "Пездюк,сокращённо-вилкой в глаз или в топку всё?"
             ,'q': "вилкой в глаз или в топку всё?"
             ,'s': set(["вилкой в глаз", "в топку всё"])}
           , {'r': "Рыбку съесть, косточкой не подавиться или лучше Настя, скажи Пездюк?"
             ,'q': "Рыбку съесть, косточкой не подавиться или лучше Настя?"
             ,'s': set(["Рыбку съесть", "косточкой не подавиться", "лучше Настя"])}
           , {'r': "Рыбку съесть, косточкой не подавиться или лучше Настя,Пездюк?"
             ,'q': "Рыбку съесть, косточкой не подавиться или лучше Настя?"
             ,'s': set(["Рыбку съесть", "косточкой не подавиться", "лучше Настя"])}
           , {'r': "Дилемма, пездюк: раз, два, раз или хардбас?"
             ,'q': "раз, два, раз или хардбас?"
             ,'s': set(["раз", "два", "хардбас"])}
           , {'r': "Овцы сыты или волки целы? Пездюк, что скажешь?"
             ,'q': "Овцы сыты или волки целы?"
             ,'s': set(["Овцы сыты", "волки целы"])}
           , {'r': "Овцы сыты или волки целы. Пездюк, что скажешь?"
             ,'q': "Овцы сыты или волки целы?"
             ,'s': set(["Овцы сыты", "волки целы"])}
           , {'r': "Овцы сыты или волки целы, Пездюк, что скажешь?"
             ,'q': "Овцы сыты или волки целы?"
             ,'s': set(["Овцы сыты", "волки целы"])}
           , {'r': "Интересно, Пездюк, кто победит: Капитан Америка, Пездюк или пиво?"
             ,'q': "Капитан Америка, Пездюк или пиво?"
             ,'s': set(["Капитан Америка", "Пездюк", "пиво"])}
           ]
    for el in data:
        try:
            q = extract_question(el['r'], "(?imu)пездюк")
        except Exception as e:
            print("Fail exception:\n\tr:%s\n\ta:%s\n\tq:%s" %(el['r'], "EXCEPTION", el['q']))
            continue
        if q != el['q']:
            print("Fail extract:\n\tr:%s\n\ta:%s\n\tq:%s" %(el['r'], q, el['q']))
        s = split_question(q)
        if s != el['s']:
            print("Fail split:\n\tr:%s\n\ta:%s\n\tq:%s" %(q, s, el['s']))
        