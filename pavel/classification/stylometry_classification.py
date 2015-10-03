__author__ = 'Pavel Soriano'
__mail__ = 'sorianopavel@gmail.com'

import numpy as np
from pavel.base_experiments.BaseExperimenter import BaseExperimenter
from models import build_sup_base_model
from sklearn import cross_validation


class StylometryClassification(BaseExperimenter):
    def __init__(self, data_path):
        self.load_data(data_path)
        df_cit = self.df[self.df.n_citations.notnull()]
        self.fr_df_cit = df_cit[df_cit["lang_title"] == "fr"]
        self.list_docs = ["../../input/pdfs/1page/{}.txt".format(f) for f in self.fr_df_cit.id.values]
        self.X, failed_ids = self.get_style_matrix(list_files=self.list_docs)
        self.y = np.where(self.fr_df_cit.n_citations > 0, 1, 0)
        print

    def classify_docs(self):
        X_train, X_test, y_train, y_test = cross_validation.train_test_split(self.X, self.y,
                                                                             test_size=0.3, random_state=0)
        clf = build_sup_base_model().fit(X_train, y_train)
        clf.score(X_test, y_test)

    @staticmethod
    def get_style_matrix(list_files):
        import sys
        failed_ids = []
        sys.path.append('../external_sources/stylometry')
        from stylometry.extract import *
        from stylometry.classify import *
        # import stylometry
        arrays_list = []
        for doc in list_files:
            try:
                style_doc = StyloDocument(doc, language="french")
            except:
                id = doc.split("/")[-1][:-4]
                failed_ids.append(id)
                pass
            arrays_list.append(style_doc.array_output())
        mat = np.vstack(arrays_list)
        return mat, failed_ids



def main():
    my_classifier = StylometryClassification(data_path="../../input/RNTI_articles_export_fixed1347_ids.txt")
    my_classifier.classify_docs()
    # my code here

if __name__ == "__main__":
    main()