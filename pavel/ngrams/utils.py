# -*- coding: utf-8 -*-
'''
Created on 27/03/2012
Module: File input & output
@author: Pavel
'''
from pavel.utils import get_files

def sort_dict(dicto, decrease=True, by_key=True):
    """
    Saves object to disk as a pickle file.
    """
    import operator
    if by_key:
        return sorted(dicto.iteritems(), key=operator.itemgetter(0), reverse=decrease)
    else:
        return sorted(dicto.iteritems(), key=operator.itemgetter(1), reverse=decrease)


def update_dict_values(orig_dict, new_dict):
    if not orig_dict:
        return new_dict
    for k, v in orig_dict.iteritems():
        print ("."),
        v.update(new_dict[k])
        orig_dict[k] = v
    print
    return orig_dict


def get_texts(path):
    import os
    from collections import defaultdict
    import ntpath

    dict_file_text = defaultdict(list)
    if os.path.isdir(path):

        # It is a path, we load all text files in this folder
        files_names = get_files(path, "txt")
        for f in files_names:
            filename = ntpath.basename(f)
            text, _ = import_text_lines(f, "utf8")
            text = text.replace('None', '')
            dict_file_text[filename] = text
        return dict_file_text
    else:
        # Path is a file
        text, _ = import_text_lines(path, "utf8")
        filename = ntpath.basename(path)
        dict_file_text[filename] = text.lower()

    return dict_file_text


def save_to_pickle(objecto, path_object=None):
    import cPickle as pickle
    try:
        pickle.dump(objecto, open(path_object, "wb"))
    except Exception, e:
        print "Could not save ", str(objecto), ":", e


def get_from_pickle(path_object):
    import cPickle as pickle
    try:
        objecto = pickle.load(open(path_object, "rb"))
    except Exception, e:
        print "Could not retrieve ", path_object, ":", e
        return None
    return objecto


def to_text_file(to_print, filename, typer="list", op="w"):
    texto = open(filename, op)
    if typer == "list":
        for thing in to_print:
            texto.write(str(thing) + "\n")
    elif typer == "dict":
        for key, value in to_print.iteritems():
            texto.write(str(key) + ": " + str(value) + "\n")
    texto.close()


'''
Import text from a file. As a single string containing all text or as a list of lines.
It assumes the input is in utf-8
'''


def import_text_lines(filename, encode=None):
    import codecs
    if encode:
        text = codecs.open(filename, 'r', encoding=encode)
    else:
        text = open(filename, 'r')
    lines = text.readlines()
    items_lines = [line.strip(u'\xef\xbb\xbf\r\n').replace(u'\n', u" ") for line in lines]
    text.seek(0)
    string = text.read()#.replace('\n', " ")
    # string = text.read()
    return string, items_lines


def print_ngrams(trigrams, measure):
    print
    print "%d-grams sorted according to %s:\n" % (len(trigrams[0][0]), measure)
    for t in trigrams:
        s = "%s : %3f" % (" ".join(t[0]), t[1])
        print s
    # print s.decode("cp1252", "ignore").encode("cp1252")
    print
