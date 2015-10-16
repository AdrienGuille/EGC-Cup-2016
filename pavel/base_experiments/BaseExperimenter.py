__author__ = 'Pavel Soriano'
__mail__ = 'sorianopavel@gmail.com'

import pandas as pd
import logging

class BaseExperimenter():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    def load_data(self, path="../../input/RNTI_articles_export_fixed1347_ids.txt"):
        egc_df = self.get_EGC_articles(path)
        self.df = egc_df
        pass

    def get_EGC_articles(self, data_path):
        egc_df = pd.read_csv(data_path, sep="\t", error_bad_lines=False, encoding="utf-8")
        return egc_df[egc_df["booktitle"] == "EGC"]
