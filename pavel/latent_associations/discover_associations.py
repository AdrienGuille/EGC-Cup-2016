__author__ = 'Pavel Soriano'
__mail__ = 'sorianopavel@gmail.com'

from collections import defaultdict

import numpy as np
from numpy.linalg import pinv
import networkx as nx

from scipy.linalg import sqrtm

from clustering.train import nmf_clustering
from ngrams.utils import load_text_data
from base_experiments.BaseExperimenter import BaseExperimenter


class DiscoverAssociations(BaseExperimenter):
    """
    Based on Discoverting Semantically associated itemsets with hypergraphs from Liu.
    """

    def __init__(self):
        self.one_pages = load_text_data("../../input/pdfs/1page/", "txt")
        # self.load_computed_topics()
        self.dict_topic_top_words, self.dict_doc_top_topics, self.dict_topic_top_docs = nmf_clustering(self.one_pages)
        # return dict_topic_top_words, dict_doc_top_topics, dict_topic_top_docs
        self.load_data()

    def load_computed_topics(self):
        import pickle
        topic_model = pickle.load(open("../input/nmf_15topics_egc.pickle", "rb"))
        pass


    def find_proper_authors(self, n_publications=5):
        """
        Find those authors that have 5 or more publications
        :return:Selected authors
        """
        from collections import Counter
        with_1page_df = self.df.iloc[[int(a) for a in self.dict_doc_top_topics.keys()]]
        self.single_authors = [b for a in with_1page_df.authors for b in a.split(", ")]
        # authors
        histo = Counter(self.single_authors)
        self.selected_authors = sorted([(k, v) for k, v in histo.iteritems() if v >= n_publications],
                                       key=lambda a: a[1], reverse=True)
        self.page1_df = with_1page_df

    def link_authors_papers_topics(self):
        """
        Find which topics represents each author. Get the top 3 topics represent each author (through its documents)

        :return:
        """

        def get_author_papers(author, id_authors):
            author_papers = [r[0] for r in id_authors if author in r[1]]
            # for row in self.page1_df.iterrows():
            #     if author in row[1].authors:
            #         author_papers.append(row[1].id)
            return author_papers

        author_topics = defaultdict(list)
        id_authors = self.page1_df[["id", "authors"]].values
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
        years = self.page1_df.year.unique()
        n_years = len(years)

        self.author_year_incidence = np.zeros((n_authors, n_years))

        for i, author_i in enumerate(self.author_topics_weighted.keys()):
            for j, year in enumerate(years):
                year_authors = self.page1_df.authors[self.page1_df.year == year].values
                for authors in year_authors:
                    if author_i in authors:
                        self.author_year_incidence[i, j] += 1

        pass

    def create_author_topic_matrix(self, n_topics_per_author=3):
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
            for t, _ in tw[:n_topics_per_author]:
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

        # self.L = self.Dv - np.dot(np.dot(self.incidence_mat, inv(self.De)), self.incidence_mat.transpose())
        L = 0.5 * (I - np.dot(np.dot(Dvsqrt, A), Dvsqrt))

        Lpinv = pinv(L)
        return Lpinv

    def find_frequent_2itemsets(self, similarity_matrix):

        ij_indices = np.where((np.triu(similarity_matrix, 1) > self.theta) & (np.triu(similarity_matrix, 1) < 1.))
        self.itemsets2 = []
        print "The are {0} 2-itemsets found. They are: ".format(len(ij_indices[0]))
        for i, j in zip(ij_indices[0], ij_indices[1]):
            self.itemsets2.append(([i, j], similarity_matrix[i, j]))

        return self.itemsets2

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
        self.sorted_itemsets = weighted_itemsets

    def print_frequent_kitemsets(self):
        for itemset, w in self.sorted_itemsets:
            stringo = ""
            for a in itemset:
                stringo += a.encode("utf-8") + ", "
            stringo = stringo[:-2] + ": " + str(w)
            print stringo

    def run(self):
        self.theta = 0.55
        self.find_proper_authors(n_publications=5)
        self.link_authors_papers_topics()

        self.create_author_topic_matrix(n_topics_per_author=4)
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
        similarity_matrix = self.author_year_similarity
        self.find_frequent_2itemsets(similarity_matrix)
        self.create_induced_graph(similarity_matrix)
        self.find_frequent_kitemsets(similarity_matrix)

        self.print_frequent_kitemsets()

    def combine_similarity_matrices(self, similarities_matrices):
        sum_matrix = reduce(np.add, similarities_matrices)
        return sum_matrix / len(similarities_matrices)


def main():
    # my code here
    assoc_discover = DiscoverAssociations()
    assoc_discover.run()


if __name__ == "__main__":
    main()
