#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals

import random
import re

def decide(choices):
    if not choices:
        return "Что?"
    if len(choices) == 1:
        r = random.randint(0,100) # 101 res, including both 0 and 100
        if r == 50:
            return "Ой всё!"
        elif r > 50:
            return "Да"
        else:
            return "Нет"
    return random.choice(choices)

def extract_question(raw_string, refer_to_regex):
    if not re.match("(?imsu).*"+refer_to_regex+".*\\?", raw_string):
        return ""

    pre_variation_regex="(?imsu)"+".*"+refer_to_regex+".*(:|-)\\s*";
    pre_rc = re.compile(pre_variation_regex)
    if pre_rc.search(raw_string):
        return pre_rc.sub("", raw_string)

    post_variation_with_pre_comma_regex = "(?imsu)"+".*[.,-].*"+refer_to_regex+"[\\s?.,-]*(.+(?:,|или|or)+.+)"
    post_pcrc = re.compile(post_variation_with_pre_comma_regex)
    post_prcr_match = post_pcrc.match(raw_string)
    if post_prcr_match:
        return post_prcr_match.group(1)

    post_variation_regex="(?imsu)"+"\\s*[?.,-][^-^,^.^?]*"+refer_to_regex+".*\\?"
    post_rc = re.compile(post_variation_regex)
    if post_rc.search(raw_string):
        return post_rc.sub("?", raw_string)

    single_comma_pre_variation_regex="(?imsu)"+"(?:.*\n?)[^,^:^-]*"+refer_to_regex+"[^,^:^-]*\\s*(,|:|-)\\s*";
    scpre_rc = re.compile(single_comma_pre_variation_regex)
    if scpre_rc.search(raw_string):
        return scpre_rc.sub("", raw_string)

def split_question(question_str):
    if question_str:
        p = re.split("(?imsu)"+"\\s*(?:,|\\sили\\s|\\sor\\s|\n)\\s*", question_str[:-1])
        return list(set(p)-set(['']))
    return []

if __name__ == '__main__':
    #in_str = raw_input("Enter a question: ")
    data = [ {'r': "Женеманс, что лучше - вилкой в глаз или в топку всё?"
             ,'q': "вилкой в глаз или в топку всё?"
             ,'s': ["вилкой в глаз", "в топку всё"]}
           , {'r': "Женеманс,сокращённо-вилкой в глаз или в топку всё?"
             ,'q': "вилкой в глаз или в топку всё?"
             ,'s': ["вилкой в глаз", "в топку всё"]}
           , {'r': "Рыбку съесть, косточкой не подавиться или лучше Настя, скажи Женеманс?"
             ,'q': "Рыбку съесть, косточкой не подавиться или лучше Настя?"
             ,'s': ["Рыбку съесть", "косточкой не подавиться", "лучше Настя"]}
           , {'r': "Рыбку съесть, косточкой не подавиться или лучше Настя,Женеманс?"
             ,'q': "Рыбку съесть, косточкой не подавиться или лучше Настя?"
             ,'s': ["Рыбку съесть", "косточкой не подавиться", "лучше Настя"]}
           , {'r': "Дилемма, женеманс: раз, два, раз или хардбас?"
             ,'q': "раз, два, раз или хардбас?"
             ,'s': ["раз", "два", "хардбас"]}
           , {'r': "Овцы сыты или волки целы? Женеманс, что скажешь?"
             ,'q': "Овцы сыты или волки целы?"
             ,'s': ["Овцы сыты", "волки целы"]}
           , {'r': "Овцы сыты или волки целы. женеманс, что скажешь?"
             ,'q': "Овцы сыты или волки целы?"
             ,'s': ["Овцы сыты", "волки целы"]}
           , {'r': "Овцы сыты или волки целы - женеманс, что скажешь?"
             ,'q': "Овцы сыты или волки целы?"
             ,'s': ["Овцы сыты", "волки целы"]}
           , {'r': "Овцы сыты или волки целы, Женеманс, что скажешь?"
             ,'q': "Овцы сыты или волки целы?"
             ,'s': ["Овцы сыты", "волки целы"]}
           , {'r': "Интересно, Женеманс, кто победит: Капитан Америка, Женеманс или пиво?"
             ,'q': "Капитан Америка, Женеманс или пиво?"
             ,'s': ["Капитан Америка", "Женеманс", "пиво"]}
           , {'r': "Екарный Женеманс, идти на работу или Настя?"
             ,'q': "идти на работу или Настя?"
             ,'s': ["идти на работу", "Настя"]}
           , {'r': "Женеманс, надо идти на работу?"
             ,'q': "надо идти на работу?"
             ,'s': ["надо идти на работу"]}
           , {'r': "Что бы ты ответил, Женеманс, надо идти на работу или лучше дома остаться?"
             ,'q': "надо идти на работу или лучше дома остаться?"
             ,'s': ["надо идти на работу", "лучше дома остаться"]}
           , {'r': """Gera typed:

        Женеманс, пора праздновать или дебажить?"""
             ,'q': "пора праздновать или дебажить?"
             ,'s': ["пора праздновать", "дебажить"]}
           , {'r': """Женеманс, какое число выберешь:
1
2
3
?"""
             ,'q': """1
2
3
?"""

             ,'s': ["1","2","3"]}
           , {'r': "Женеманс, тест без вопроса"
             ,'q': ""
             ,'s': []}
           , {'r': "Женеманс, Филипс или Tornado?"
             ,'q': "Филипс или Tornado?"
             ,'s': ["Филипс", "Tornado"]}
           ]
    for el in data:
        q = extract_question(el['r'], "(?imsu)Женеманс")
        if q != el['q']:
            print("Fail extract:\n\tr:%s\n\ta:%s\n\tq:%s" %(el['r'], q, el['q']))
            continue
        s = split_question(q)
        if set(s) != set(el['s']):
            print("Fail split:\n\tr:%s\n\ta:%s\n\tq:%s" %(q, s, el['s']))
#        print(el['r'], "->", decide(s))
