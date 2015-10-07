__author__ = 'Pavel Soriano'
__mail__ = 'sorianopavel@gmail.com'

import numpy as np
from pavel.base_experiments.BaseExperimenter import BaseExperimenter
from models import build_sup_base_model
from sklearn import cross_validation


class StylometryClassification(BaseExperimenter):
    def __init__(self, data_path):
        self.load_data(data_path)
        self.df = self.df[self.df.n_citations.notnull()]
        # self.fr_df_cit = df_cit[df_cit["lang_title"] == "fr"]
        self.list_docs = ["../../input/pdfs/full/{}.txt".format(f) for f in self.df.id]
        self.X, with_doc_ids = self.get_style_matrix(list_files=self.list_docs)
        self.y = np.where(self.df.n_citations.values[with_doc_ids] > 0, 1, 0)
        print

    def classify_docs(self):
        X_train, X_test, y_train, y_test = cross_validation.train_test_split(self.X, self.y,
                                                                             test_size=0.3, )
        clf = build_sup_base_model().fit(X_train, y_train)
        # print("Residual sum of squares: %.2f"% np.mean((clf.predict(X_test) - y_test) ** 2))
        y_hat = clf.predict(X_test)
        print clf.score(X_test, y_test)


    @staticmethod
    def get_style_matrix(list_files):
        import sys
        with_doc_ids = []
        sys.path.append('../external_sources/stylometry')
        from stylometry.extract import *
        from stylometry.classify import *
        # import stylometry
        arrays_list = []
        for doc in list_files:
            has_doc = False
            # id = doc.split("/")[-1][:-4]
            try:
                style_doc = StyloDocument(doc, language="french")
                has_doc = True
            except:
                continue
            with_doc_ids.append(has_doc)
            arrays_list.append(style_doc.array_output())
        mat = np.vstack(arrays_list)
        return mat, np.array(with_doc_ids, dtype=np.bool)



def main():
    my_classifier = StylometryClassification(data_path="../../input/RNTI_articles_export_fixed1347_ids.txt")
    my_classifier.classify_docs()
    # my code here

if __name__ == "__main__":
    main()