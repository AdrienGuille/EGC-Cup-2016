#!/usr/bin/env python
# coding: utf8

import time
from random import randint
import pandas as pd

from scholar import query


def get_EGC_articles(data_path):
    egc_df = pd.read_csv(data_path, sep="\t", error_bad_lines=False, encoding="utf-8")
    return egc_df[egc_df["booktitle"] == "EGC"]


# def load_data_egc(data_path):
#     egc_df = pd.read_csv(data_path, sep="\t", error_bad_lines=False, encoding="utf-8")
#     return egc_df


class GetGScholarInfo():
    def __init__(self, df=None):
        if df is not None:
            self.df = df
        else:
            self.load_data()

    def load_data(self):
        egc_df = get_EGC_articles("../../input/RNTI_articles_export_fixed1347_ids.txt")
        self.df = egc_df
        pass

    def get_gscholar_n_citations(self, title, wait=True):
        if wait:
            time.sleep(randint(10, 20))
        return query(title)

    def load_citations_disk(self):
        import cPickle as pickle
        try:
            citations = pickle.load(open("./external_sources/citations.pkl", 'rb'))
            return citations
        except:
            raise IOError("Could not load dictionary of citations.")
            return {}

    def save_citations_disk(self, data):
        import cPickle as pickle
        pickle.dump(data, open("./external_sources/citations.pkl", 'wb'))

    def run(self, from_disk=True):

        citations_list = []
        citations_dic = self.load_citations_disk()
        for row in self.df.iterrows():
            title = row[1]["title"]
            id = row[1]["id"]
            n_citations = citations_dic.get(id, "")
            if not from_disk or not citations_dic:
                if id in citations_dic:
                    n_citations = citations_dic[id]
                else:
                    n_citations = self.get_gscholar_n_citations(title)

                    if int(n_citations) < 0:
                        n_citations = ""
                        print "{} not succeded".format(title.encode("utf-8"))
                    else:
                        print "{} succeded".format(title.encode("utf-8"))
                        citations_dic[id] = n_citations
                        self.save_citations_disk(citations_dic)
            citations_list.append(n_citations)
        self.df["n_citations"] = citations_list
        self.df.to_csv("../input/RNTI_articles_export_fixed1347_ids.txt", sep="\t", encoding="utf-8",
                       index=False,
                       index_label=False)
        return self.df


def main():
    # my code here
    migs = GetGScholarInfo()
    migs.run()


if __name__ == "__main__":
    main()
