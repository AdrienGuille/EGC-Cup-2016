# coding: utf-8
__author__ = "Adrien Guille"
__email__ = "adrien.guille@univ-lyon2.fr"

import re


def references(string):
    string = string.replace(u'∗', u'*')
    m = re.findall('\*{1,5}[\s|,]+', string)
    for i in range(len(m)):
        m[i] = m[i].replace(' ', '').replace('\n', '').replace(',', '')
    return m

def find_affiliation(reference, text):
    print 'test'


def to_simple_ranking(weighted_list):
    ranking = []
    for weighted_author in weighted_list:
        ranking.append(weighted_author[0])
    return ranking


def ranking_evolution(ranking0, ranking1):
    evolution = []
    for rank1 in range(0, len(ranking0)):
        author = ranking1[rank1]
        ev = "new"
        if author in ranking0:
            ev = ranking0.index(author) - rank1
        evolution.append([author, ev])
    return evolution
