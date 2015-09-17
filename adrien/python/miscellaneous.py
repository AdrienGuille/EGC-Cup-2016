# coding: utf-8
__author__ = "Adrien Guille"
__email__ = "adrien.guille@univ-lyon2.fr"

import re
from scipy import stats


def references(string):
    m = re.findall('\*{1,5}[\s|,]+', string)
    for i in range(len(m)):
        m[i] = m[i].replace(' ', '').replace('\n', '').replace(',', '')
    return m


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


def average_distribution(dist0, dist1):
    dist2 = []
    for i in range(0, len(dist0)):
        dist2.append((dist0[i]+dist1[i])*0.5)
    return dist2


def jensen_shannon_divergence(dist0, dist1):
    average_dist = average_distribution(dist0, dist1)
    kl_divergence0 = stats.entropy(dist0, average_dist)
    kl_divergence1 = stats.entropy(dist1, average_dist)
    return (kl_divergence0+kl_divergence1)/2.0
