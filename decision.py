#!/usr/bin/python
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
        return ""

    pre_variation_regex="(?imsu)"+".*"+refer_to_regex+".*(:|-)\\s*";
    pre_rc = re.compile(pre_variation_regex)
    if pre_rc.search(raw_string):
        return pre_rc.sub("", raw_string)

    post_variation_regex="(?imsu)"+"[?.,][^,^.^?]*"+refer_to_regex+".*\\?"
    post_rc = re.compile(post_variation_regex)
    if post_rc.search(raw_string):
        return post_rc.sub("?", raw_string)

    single_comma_pre_variation_regex="(?imsu)"+"(?:.*\n?)[^,^:^-]*"+refer_to_regex+"[^,^:^-]*\\s*(,|:|-)\\s*";
    scpre_rc = re.compile(single_comma_pre_variation_regex)
    if scpre_rc.search(raw_string):
        return scpre_rc.sub("", raw_string)

def split_question(question_str):
    p = re.split("\\s?(?:,|или|or)\\s?", question_str[:-1])
    return list(set(p))

if __name__ == '__main__':
    #in_str = raw_input("Enter a question: ")
    data = [ {'r': "Пездюк, что лучше - вилкой в глаз или в топку всё?"
             ,'q': "вилкой в глаз или в топку всё?"
             ,'s': ["вилкой в глаз", "в топку всё"]}
           , {'r': "Пездюк,сокращённо-вилкой в глаз или в топку всё?"
             ,'q': "вилкой в глаз или в топку всё?"
             ,'s': ["вилкой в глаз", "в топку всё"]}
           , {'r': "Рыбку съесть, косточкой не подавиться или лучше Настя, скажи Пездюк?"
             ,'q': "Рыбку съесть, косточкой не подавиться или лучше Настя?"
             ,'s': ["Рыбку съесть", "косточкой не подавиться", "лучше Настя"]}
           , {'r': "Рыбку съесть, косточкой не подавиться или лучше Настя,Пездюк?"
             ,'q': "Рыбку съесть, косточкой не подавиться или лучше Настя?"
             ,'s': ["Рыбку съесть", "косточкой не подавиться", "лучше Настя"]}
           , {'r': "Дилемма, пездюк: раз, два, раз или хардбас?"
             ,'q': "раз, два, раз или хардбас?"
             ,'s': ["раз", "два", "хардбас"]}
           , {'r': "Овцы сыты или волки целы? Пездюк, что скажешь?"
             ,'q': "Овцы сыты или волки целы?"
             ,'s': ["Овцы сыты", "волки целы"]}
           , {'r': "Овцы сыты или волки целы. Пездюк, что скажешь?"
             ,'q': "Овцы сыты или волки целы?"
             ,'s': ["Овцы сыты", "волки целы"]}
           , {'r': "Овцы сыты или волки целы, Пездюк, что скажешь?"
             ,'q': "Овцы сыты или волки целы?"
             ,'s': ["Овцы сыты", "волки целы"]}
           , {'r': "Интересно, Пездюк, кто победит: Капитан Америка, Пездюк или пиво?"
             ,'q': "Капитан Америка, Пездюк или пиво?"
             ,'s': ["Капитан Америка", "Пездюк", "пиво"]}
           , {'r': "Екарный Пездюк, идти на работу или Настя?"
             ,'q': "идти на работу или Настя?"
             ,'s': ["идти на работу", "Настя"]}
           , {'r': "Пездюк, надо идти на работу?"
             ,'q': "надо идти на работу?"
             ,'s': ["надо идти на работу"]}
           , {'r': """Gera typed:

        Пездюк, пора праздновать или дебажить?"""
             ,'q': "пора праздновать или дебажить?"
             ,'s': ["пора праздновать","дебажить"]}
           ]
    for el in data:
        q = extract_question(el['r'], "(?imsu)пездюк")
        if q != el['q']:
            print("Fail extract:\n\tr:%s\n\ta:%s\n\tq:%s" %(el['r'], q, el['q']))
            continue
        s = split_question(q)
        if set(s) != set(el['s']):
            print("Fail split:\n\tr:%s\n\ta:%s\n\tq:%s" %(q, s, el['s']))
        print(el['r'], "->", decide(s))
