__author__ = 'Pavel Soriano'
__mail__ = 'sorianopavel@gmail.com'

from collections import defaultdict

import numpy as np
from numpy.linalg import pinv, inv
import networkx as nx
from scipy.linalg import sqrtm

from clustering.train import nmf_clustering
from base_experiments.BaseExperimenter import BaseExperimenter


class DiscoverAssociations(BaseExperimenter):
    """
    Based on Discoverting Semantically associated itemsets with hypergraphs from Liu.
    """

    def __init__(self, theta, min_n_papers_per_author, n_topics_per_author):
        self.load_computed_topics()
        # self.dict_topic_top_words, self.dict_doc_top_topics, self.dict_topic_top_docs = nmf_clustering(self.one_pages)
        feature_names = zip(*sorted(self.topic_model.corpus.vocabulary.items(), key=lambda a: a[0]))[1]

        self.dict_topic_top_words, \
        self.dict_doc_top_topics, \
        self.dict_topic_top_docs = nmf_clustering(data=None, doc_topic_mat=self.topic_model.document_topic_matrix,
                                                  topic_token_mat=self.topic_model.topic_word_matrix,
                                                  feature_names=feature_names)
        # return dict_topic_top_words, dict_doc_top_topics, dict_topic_top_docs
        self.load_data()
        self.theta = theta
        self.min_publications_per_author = min_n_papers_per_author
        self.n_topics_per_author = n_topics_per_author

    def load_computed_topics(self):
        import pickle
        import sys
        sys.path.append("/media/stuff/Pavel/Documents/Eclipse/workspace/TOM/")
        self.topic_model = pickle.load(open("../input/nmf_15topics_egc.pickle", "rb"))

    def find_proper_authors(self):
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
        histo = Counter(self.single_authors)
        self.selected_authors = sorted([(k, v) for k, v in histo.iteritems() if v >= self.min_publications_per_author],
                                       key=lambda a: a[1], reverse=True)

        self.logger.info("{} selected authors".format(len(self.selected_authors)))

    def link_authors_papers_topics(self):
        """
        Find which topics represents each author. Get the top 3 topics represent each author (through its documents)

        :return:
        """

        def get_author_papers(author, id_authors):
            author_papers = [r[0] for r in id_authors if author in r[1]]
            return author_papers

        author_topics = defaultdict(list)
        id_authors = zip(range(len(self.all_authors)), self.all_authors)

        for author, n_papers in self.selected_authors:
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

    def create_author_year_matrix(self):
        n_authors = self.author_topics_weighted.keys().__len__()
        years = self.df.year.unique()
        n_years = len(years)

        self.author_year_incidence = np.zeros((n_authors, n_years))

        for i, author_i in enumerate(self.author_topics_weighted.keys()):
            for j, year in enumerate(years):
                year_authors = self.df.authors[self.df.year == year].values
                for authors in year_authors:
                    if author_i in authors:
                        self.author_year_incidence[i, j] += 1

        pass

    def create_author_topic_matrix(self):
        """
        The topic author matrix is in fact my incidence matrix where the rows are the vertices (authors) and the
        hyperedges are the topics
        :param n_topics_per_author:
        :return:
        """
        self.author_topic_incidence = np.zeros((self.author_topics_weighted.keys().__len__(),
                                                self.dict_topic_top_words.keys().__len__()))
        # for i in range(self.dict_topic_top_words.keys()):
        #     for jx, (author, tw) in enumerate(range(self.author_topics_weighted)):
        #         top_n_topics_author = self.author_topics_weighted[author]
        #         pass

        for i_x, (author, tw) in enumerate(self.author_topics_weighted.iteritems()):
            for t, _ in tw[:self.n_topics_per_author]:
                self.author_topic_incidence[i_x, t] = 1

        self.author_topic_incidence = self.author_topic_incidence

    def vertex_degree_diagonal_matrix(self, incidence_matrix):
        return np.diag(incidence_matrix.sum(axis=1))

    def edge_degree_diagonal_matrix(self, incidence_matrix):
        return np.diag(incidence_matrix.sum(axis=0))

    def create_laplacian_pseudo_inverse(self, incidence_matrix, Dv, De):
        """
        Based on the forumula used by the author : L = Dv - HWDe^-1H'


        :return:
        """
        I = np.eye(Dv.shape[0])
        A = np.dot(incidence_matrix, incidence_matrix.transpose()) - Dv
        Dvsqrt = sqrtm(Dv)

        # L = Dv - np.dot(np.dot(incidence_matrix, inv(De)), incidence_matrix.transpose())
        L = 0.5 * (I - np.dot(np.dot(Dvsqrt, A), Dvsqrt))
        # L = I - (.5* inv(Dvsqrt)).dot(incidence_matrix).dot(incidence_matrix.transpose()).dot(inv(Dvsqrt))

        Lpinv = pinv(L)
        return Lpinv

    def find_frequent_2itemsets(self, similarity_matrix):

        ij_indices = np.where((np.triu(similarity_matrix, 1) > self.theta))
        self.logger.info("The are {0} 2-itemsets found. They are: ".format(len(ij_indices[0])))
        k2itemsets = zip(ij_indices[0], ij_indices[1])
        # for i, j in zip(ij_indices[0], ij_indices[1]):
        #     self.itemsets2.append(([i, j], similarity_matrix[i, j]))
        #     print self.itemsets2[-1]
        #
        weighted_itemsets = []
        for sub in k2itemsets:
            itemsets_sum = []
            authors = [self.author_topics_weighted.keys()[i] for i in sub]
            # authors = [self.author_topics_weighted.keys()[i] + ":" + unicode(i) for i in sub]

            for i_i in range(len(sub) - 1):
                for j_j in range(i_i + 1, len(sub)):
                    itemsets_sum.append(similarity_matrix[sub[i_i], sub[j_j]])
            weighted_itemsets.append((authors, np.mean(itemsets_sum)))
        weighted_itemsets.sort(key=lambda a: a[1], reverse=True)
        self.sorted_2itemsets = weighted_itemsets
        return self.sorted_2itemsets

    def create_similarity_ct(self, Lpinv, Dv):
        """
        Create the commute time similarity matrix: n(i,j) = VG(l_ii + l_jj -2l_ij)
        VG = tr(Dv)
        :return:
        """
        trace_L = Lpinv.diagonal()
        l_jj, l_ii = np.meshgrid(trace_L, trace_L)

        vol_Dv = Dv.trace()

        dist_ct = vol_Dv * (l_ii + l_jj - (2 * Lpinv))
        # Treat negative values
        if dist_ct.min() < 0:
            dist_ct = dist_ct + abs(dist_ct.min())
            np.fill_diagonal(dist_ct, 0.)

        sim_ct = 1. - (dist_ct / np.max(dist_ct, axis=1)[:, None])

        return sim_ct

    def create_induced_graph(self, similarity_matrix):
        g = nx.Graph()
        # g.add_nodes_from(range(self.incidence_mat.shape[0]))

        n = similarity_matrix.shape[0]
        for i in range(n - 1):
            for j in range(i + 1, n):
                shared_hyperedges = np.intersect1d(np.where(self.author_topic_incidence[i, :] > 0),
                                                   np.where(self.author_topic_incidence[j, :] > 0))
                if len(shared_hyperedges) > 0 and similarity_matrix[i, j] > self.theta:
                    g.add_edge(i, j)
        self.induced_g = g
        return self.induced_g

    def find_frequent_kitemsets(self, similarity_matrix):
        if not hasattr(self, "induced_g"):
            raise Exception("No induced graph available. Aborting")

        cliques = list(nx.find_cliques(self.induced_g))
        connected_components = list(nx.connected_components(self.induced_g))

        subgraphs = cliques + connected_components
        weighted_itemsets = []
        for sub in subgraphs:
            itemsets_sum = []
            authors = [self.author_topics_weighted.keys()[i] for i in sub]
            for i_i in range(len(sub) - 1):
                for j_j in range(i_i + 1, len(sub)):
                    itemsets_sum.append(similarity_matrix[sub[i_i], sub[j_j]])
            weighted_itemsets.append((authors, np.mean(itemsets_sum)))
        # weighted_itemsets = list(set(weighted_itemsets))
        weighted_itemsets.sort(key=lambda a: a[1], reverse=True)
        # self.sorted_itemsets = weighted_itemsets
        return weighted_itemsets

    def print_frequent_kitemsets(self, sorted_itemsets):
        for itemset, w in sorted_itemsets:
            stringo = ""
            for a in itemset:
                stringo += a.encode("utf-8") + ", "
            stringo = stringo[:-2] + ": " + str(w)
            print stringo

    def run(self):

        self.find_proper_authors()
        self.link_authors_papers_topics()

        self.create_author_topic_matrix()
        self.create_author_year_matrix()

        self.author_topic_Dv = self.vertex_degree_diagonal_matrix(self.author_topic_incidence)
        self.author_topic_De = self.edge_degree_diagonal_matrix(self.author_topic_incidence)

        self.author_year_Dv = self.vertex_degree_diagonal_matrix(self.author_year_incidence)
        self.author_year_De = self.edge_degree_diagonal_matrix(self.author_year_incidence)

        self.author_topic_Lpinv = self.create_laplacian_pseudo_inverse(self.author_topic_incidence,
                                                                       self.author_topic_Dv,
                                                                       self.author_topic_De)

        self.author_year_Lpinv = self.create_laplacian_pseudo_inverse(self.author_year_incidence,
                                                                      self.author_year_Dv,
                                                                      self.author_year_De)

        self.author_topic_similarity = self.create_similarity_ct(self.author_topic_Lpinv, self.author_topic_Dv)
        self.author_year_similarity = self.create_similarity_ct(self.author_year_Lpinv, self.author_year_Dv)

        combined_similarity = self.combine_similarity_matrices(
            [self.author_topic_similarity, self.author_year_similarity])
        similarity_matrix = combined_similarity
        similarity_matrix = self.author_topic_similarity
        # similarity_matrix = self.author_year_similarity

        k2itemsets = self.find_frequent_2itemsets(similarity_matrix)

        # Find k>3 itemsets
        # self.create_induced_graph(similarity_matrix)
        # knitemsets = self.find_frequent_kitemsets(similarity_matrix)

        self.print_frequent_kitemsets(k2itemsets)
        return self.evaluate_latent_itemsets(k2itemsets), len(k2itemsets), len(self.selected_authors)

    def combine_similarity_matrices(self, similarities_matrices):
        sum_matrix = reduce(np.add, similarities_matrices)
        return sum_matrix / len(similarities_matrices)

    def evaluate_latent_itemsets(self, k2itemsets):
        matches = []
        for items in k2itemsets:
            for existing_authors in self.all_authors:
                if len(set(items[0]).intersection(existing_authors)) >= 2:
                    matches.append(items)
                    break
        self.logger.info(" Number of matched existing authors sets: {}".format(len(matches)))
        print matches
        return len(matches)

    @staticmethod
    def run_grid_search():
        import pandas as pd
        gs_theta = np.arange(0.4, 0.9, 0.05)
        gs_min_n_papers_per_author = range(3, 9)  # 3 to 8 gamma
        gs_n_topics_per_author = range(2, 16)  # lambda
        from itertools import product
        grid_search_values = list(product(gs_theta, gs_min_n_papers_per_author, gs_n_topics_per_author))
        df = pd.DataFrame(
            columns=["theta", "min_n_papers", "n_topics_per_author", "true_collaborations",
                     "total_found", "ratio_true_found", "n_authors"],
            index=range(len(grid_search_values)))
        for idx, (theta, min_papers, topics_author) in enumerate(grid_search_values):
            assoc_discover = DiscoverAssociations(theta=theta, min_n_papers_per_author=min_papers,
                                                  n_topics_per_author=topics_author)

            n_true_collaborations, itemsets_found, n_authors = assoc_discover.run()
            if itemsets_found:
                ratio_true_found = float(n_true_collaborations) / itemsets_found
            else:
                ratio_true_found = 0.
            df.loc[idx] = pd.Series({"theta": theta, "min_n_papers": min_papers,
                                     "n_topics_per_author": topics_author,
                                     "true_collaborations": n_true_collaborations,
                                     "total_found": itemsets_found,
                                     "ratio_true_found": ratio_true_found,
                                     "n_authors": n_authors})

        df.to_csv("gsearch_discover_associations.csv")


def main():
    # my code here
    # DiscoverAssociations.run_grid_search()
    #
    assoc_discover = DiscoverAssociations(theta=0.6, min_n_papers_per_author=8, n_topics_per_author=2)
    assoc_discover.run()


if __name__ == "__main__":
    main()
