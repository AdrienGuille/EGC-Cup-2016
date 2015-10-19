# encoding:utf-8
from collections import defaultdict
from itertools import chain
from clustering.train import nmf_clustering
import numpy as np

__author__ = 'Pavel Soriano'
__mail__ = 'sorianopavel@gmail.com'

from base_experiments.BaseExperimenter import BaseExperimenter
import graphlab as gl


class BipartiteRecommendation(BaseExperimenter):
    def __init__(self, min_publications_per_author, topics_per_author):
        self.load_data()
        self.get_computed_TOM()
        self.min_publications_per_author = min_publications_per_author
        self.n_topics_per_author = topics_per_author
        feature_names = zip(*sorted(self.topic_model.corpus.vocabulary.items(), key=lambda a: a[0]))[1]
        self.dict_topic_top_words, \
        self.dict_doc_top_topics, \
        self.dict_topic_top_docs = nmf_clustering(data=None, doc_topic_mat=self.topic_model.document_topic_matrix,
                                                  topic_token_mat=self.topic_model.topic_word_matrix,
                                                  feature_names=feature_names)

    def filter_authors(self):
        """
        Find those authors that have 5 or more publications
        :return:Selected authors
        """
        from collections import Counter
        from itertools import chain

        n_docs = self.topic_model.document_topic_matrix.shape[0]
        self.all_authors = [self.topic_model.corpus.authors(a) for a in range(n_docs)]
        self.single_authors = list(chain.from_iterable(self.all_authors))

        # self.single_authors = [b for a in self.df.authors for b in a.split(", ")]

        # authors
        self.authors_paper_count = Counter(self.single_authors)
        self.selected_authors = sorted(
            [(k, v) for k, v in self.authors_paper_count.iteritems() if v >= self.min_publications_per_author],
            key=lambda a: a[1], reverse=True)

        self.logger.info("{} selected authors".format(len(self.selected_authors)))

    def get_authors_by_topics_weights(self, selected_authors):
        """
        Find which topics represents each author. Get the top 3 topics represent each author (through its documents)

        :return:
        """
        if not selected_authors:
            selected_authors = self.selected_authors

        def get_author_papers(author, id_authors):
            author_papers = [r[0] for r in id_authors if author in r[1]]
            return author_papers

        author_topics = defaultdict(list)
        id_authors = zip(range(len(self.all_authors)), self.all_authors)

        for author, n_papers in selected_authors:
            author_papers = get_author_papers(author, id_authors)
            for v in author_papers:
                author_topics[author].append([t[0] for t in self.dict_doc_top_topics[v] if t[1] > 0])

        # Weight the topics and choose one for each author
        self.author_topics_weighted = {}
        for author, list_topics in author_topics.iteritems():
            temp_dict = defaultdict(int)
            for topics in list_topics:
                for pos, topic in enumerate(topics):
                    temp_dict[topic] += (len(topics) - pos) / float(len(topics))
            self.author_topics_weighted[author] = sorted(temp_dict.items(), key=lambda x: x[1], reverse=True)
        print

    def build_relation_sframe(self):
        authors = []
        topics_ids = []
        weights = []
        for author, topics_weights in self.author_topics_weighted.iteritems():
            for topic_id, weight in topics_weights[:self.n_topics_per_author]:
                authors.append(author)
                topics_ids.append(topic_id)
                weights.append(weight)

        self.data = gl.SFrame({"author": authors, "topic_id": topics_ids, "weight": weights})

    def test_recommenders(self):
        import matplotlib.pyplot as plt
        # Split the data in train, test
        (train_set, test_set) = self.data.random_split(0.8)

        # Train baseline popularity recommender
        m = gl.popularity_recommender.create(train_set, 'author', 'topic_id', 'weight')
        # Test it!
        baseline_rmse = gl.evaluation.rmse(test_set['weight'], m.predict(test_set))
        print baseline_rmse
        regularization_vals = [.99, 0.1, 0.01, 0.001, 0.0001]
        models = [gl.factorization_recommender.create(train_set, 'author', 'topic_id', 'weight',
                                                      max_iterations=50, num_factors=5, regularization=r)
                  for r in regularization_vals]

        # Save the train and test RMSE, for each model
        (rmse_train, rmse_test) = ([], [])
        for m in models:
            rmse_train.append(m['training_rmse'])
            rmse_test.append(gl.evaluation.rmse(test_set['weight'], m.predict(test_set)))

        (fig, ax) = plt.subplots(figsize=(10, 8))
        [p1, p2, p3] = ax.semilogx(regularization_vals, rmse_train,
                                   regularization_vals, rmse_test,
                                   regularization_vals, len(regularization_vals) * [baseline_rmse]
                                   )
        ax.set_ylim([0, 5])
        ax.set_xlabel('Regularization', fontsize=20)
        ax.set_ylabel('RMSE', fontsize=20)
        ax.legend([p1, p2, p3], ["Train", "Test", "Baseline"])
        plt.show()
        pass

    def train_recommender(self, author_list):
        msim_cosine = gl.item_similarity_recommender.create(self.data, 'topic_id', 'author', 'weight',
                                                            similarity_type="cosine")
        results_ratio, existing_collabs = self.evaluate_recommendation(msim_cosine, author_list)
        results_ratio = np.mean(results_ratio)
        # selected_authors = [u"Djamel Abdelkader Zighed",u"Marc Plantevit",u"Gilbert Ritschard",
        #  u"Frédéric Flouvat",u"Jean-François Boulicaut",u"Gilbert Ritschard",u"Frédéric Flouvat",u"Sandra Bringay",u"Sandra Bringay"]
        all_recoms_l = [msim_cosine.get_similar_items([a[0]])[:3] for a in author_list]
        all_recoms = gl.SFrame()
        for l in all_recoms_l:
            all_recoms = all_recoms.append(l)

        # all_recoms = msim_cosine.get_similar_items().sort("score", False)
        unique_recoms = []
        for recoms in all_recoms:
            contrib = [recoms["author"], recoms["similar"]]
            contrib.sort()
            # contrib = "{0},{1}".format(contrib[0], contrib[1])
            if contrib not in unique_recoms:
                unique_recoms.append(contrib)

        pass
        return unique_recoms, existing_collabs

    def show_recomnedations(self, recoms, existing):

        def shorten_name(name):
            full_name = name.split(" ")
            return "{0}. {1}".format(full_name[0][0], full_name[1])

        g = gl.SGraph()
        existing.sort()
        recoms.sort()
        list_existing = []
        for recom in recoms:
            g = g.add_edges(gl.Edge(shorten_name(recom[0]), shorten_name(recom[1])))
            if recom in existing:
                list_existing.append(1)
            else:
                list_existing.append(0)
        pass
        g.show(vlabel="id")
        print

    def evaluate_recommendation(self, recom, selected_authors=None, n_recommendations=10):
        all_ratios = []
        if not selected_authors:
            selected_authors = self.selected_authors

        exisiting_collabs_list = []
        for a in selected_authors:
            n_existing_collabs = 0
            a_papers = self.topic_model.corpus.documents_by_author(a[0])
            a_collabs = [self.topic_model.corpus.authors(b) for b in a_papers]
            try:
                a_recoms = recom.get_similar_users(gl.SArray([a[0]]), 1000).sort("distance")[:n_recommendations]
            except:
                a_recoms = recom.get_similar_items(gl.SArray([a[0]]), n_recommendations)
            pass
            a_similar = a_recoms["similar"]

            for sim in a_similar:
                for collabs in a_collabs:
                    if sim in collabs:
                        n_existing_collabs += 1
                        if not [a[0], sim] in exisiting_collabs_list and not [sim, a[0]] in exisiting_collabs_list:
                            exisiting_collabs_list.append(sorted([a[0], sim]))
                        break
            all_ratios.append(float(n_existing_collabs) / (len(a_recoms) + .00001))
        return all_ratios, exisiting_collabs_list

    def test_recommenders_ratio(self):

        # realMarc = self.topic_model.corpus.documents_by_author(author)

        m_fact = gl.factorization_recommender.create(self.data, 'author', 'topic_id', 'weight',
                                                     regularization=10e-2)
        msim_cosine = gl.item_similarity_recommender.create(self.data, 'topic_id', 'author', 'weight',
                                                            similarity_type="cosine")
        msim_jac = gl.item_similarity_recommender.create(self.data, 'topic_id', 'author', 'weight')
        msim_pearson = gl.item_similarity_recommender.create(self.data, 'topic_id', 'author', 'weight',
                                                             similarity_type="pearson")

        recommenders = {"factorization": m_fact, "jaccard": msim_jac, "pearson": msim_pearson, "cosine": msim_cosine}
        results_ratio = {}
        for type, model in recommenders.iteritems():
            results_ratio[type] = np.mean(self.evaluate_recommendation(model))

    def get_young_authors(self, max_pubs, from_year=2012, min_pubs=2):
        """
        Find those authors that have published 3 or less papers from from_year
        :param k: Number of authors to get
        :param from_year: From which year to get them
        :return: List of young authors
        """
        from collections import Counter
        import pickle
        try:
            young_authors = pickle.load(open("young_authors.pik", "rb"))
        except:
            years = self.topic_model.corpus.data_frame["date"].unique()[::-1]
            n_docs = self.topic_model.document_topic_matrix.shape[0]
            all_authors = [self.topic_model.corpus.authors(a) for a in range(n_docs)]
            single_authors = list(chain.from_iterable(all_authors))

            authors_paper_count = Counter(single_authors)
            selected_authors = sorted([(k, v) for k, v in authors_paper_count.iteritems() if max_pubs >= v >= 2],
                                      key=lambda a: a[1])
            young_authors = defaultdict(list)
            for a, paper_count in selected_authors:
                for y in range(min(years), max(years) + 1):
                    if self.topic_model.corpus.documents_by_author(a, y):
                        young_authors[a].append(y)
        young_authors = [(k, len(v)) for k, v in young_authors.iteritems() if
                         min(v) >= from_year and len(v) >= min_pubs]

        return young_authors

    def get_confirmed_authors(self, k):
        return self.selected_authors[:k]

    def run(self):
        self.filter_authors()
        confirmed = self.get_confirmed_authors(k=10)
        young = self.get_young_authors(max_pubs=10, from_year=2012)
        target_authors = [confirmed, young]
        for ta in target_authors:
            self.get_authors_by_topics_weights(ta)
            self.build_relation_sframe()
            # self.test_recommenders()
            # self.test_recommenders_ratio()
            recoms, existing_recoms = self.train_recommender(ta)
            self.show_recomnedations(recoms, existing_recoms)


def main():
    # my code here
    brecom = BipartiteRecommendation(min_publications_per_author=5, topics_per_author=7)
    brecom.run()
    pass


main()
if __name__ == "__main__":
    pass
