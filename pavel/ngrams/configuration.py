# -*- coding: latin-1 -*-
'''
Created on Feb 12, 2014

@author: pavelo
'''
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('config.cfg')

config_path = config.get("Configuration", "text_path")
config_ngram = config.getint("Configuration", "ngram_n")
config_output = config.get("Configuration", "output_path")
config_stem = config.getboolean("Configuration", "stem")
config_min_tok_len = config.getint("Configuration", "ngram_min_tok_len")
config_min_tok_freq = config.getint("Configuration", "ngram_min_tok_freq")
config_top_k = config.getint("Configuration", "ngram_top_k")
try:
    config_stopwords = config.getboolean("Configuration", "stopwords")
    config_bool_stopwords = False
except:
    config_stopwords = config.get("Configuration", "stopwords")
    config_bool_stopwords = True
