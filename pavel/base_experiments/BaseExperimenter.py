__author__ = 'Pavel Soriano'
__mail__ = 'sorianopavel@gmail.com'

import pandas as pd
import logging

class BaseExperimenter():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    def load_data(self, path="../../input/RNTI_articles_export_lemmas2.csv"):
        egc_df = self.get_EGC_articles(path)
        self.df = egc_df
        pass

    def get_EGC_articles(self, data_path):
        egc_df = pd.read_csv(data_path, sep="\t", error_bad_lines=False, encoding="utf-8")
        return egc_df[egc_df["booktitle"] == "EGC"]

    def get_computed_TOM(self):
        import pickle
        import sys
        sys.path.append("/media/stuff/Pavel/Documents/Eclipse/workspace/TOM/")
        self.topic_model = pickle.load(open("../input/nmf_15topics_egc.pickle", "rb"))
