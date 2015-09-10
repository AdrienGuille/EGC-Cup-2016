# coding: utf-8
__author__ = "Adrien Guille"
__email__ = "adrien.guille@univ-lyon2.fr"

import pickle
import codecs


def load(lexicon_path='../../input/OLDlexique.txt'):
    input_file = codecs.open(lexicon_path, 'r', encoding='latin1')
    table = {}
    count = 0
    for line in input_file:
        line = line.lower()
        entry = line.split('\t')
        if entry[1] != '=':
            table[entry[0]] = entry[1]
            count += 1
    return table


class Lexicon:

    def __init__(self, update_data=False):
        if update_data:
            self.table = load()
            pickle.dump(self.table, open('../../output/lexicon.pickle', 'wb'))
        else:
            self.table = pickle.load(open('../../output/lexicon.pickle', 'rb'))

    def get_lem(self, word):
        if self.table.get(word):
            return self.table[word]
        else:
            return None
