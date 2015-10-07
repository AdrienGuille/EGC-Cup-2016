__author__ = 'Pavel Soriano'
__mail__ = 'sorianopavel@gmail.com'

from collections import defaultdict
from clustering.train import nmf_clustering
from ngrams.utils import load_text_data
import numpy as np

from base_experiments.BaseExperimenter import BaseExperimenter


class DiscoverAssociations(BaseExperimenter):
    def __init__(self):
        self.one_pages = load_text_data("../../input/pdfs/1page/", "txt")
        self.dict_topic_top_words, self.dict_doc_top_topics, self.dict_topic_top_docs = nmf_clustering(self.one_pages)
        # return dict_topic_top_words, dict_doc_top_topics, dict_topic_top_docs
        self.load_data()

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

    def create_topic_author_matrix(self, n_topics_per_author=3):
        incidence_mat = np.zeros((self.dict_topic_top_words.keys().__len__(),
                                  self.author_topics_weighted.keys().__len__()))
        # for i in range(self.dict_topic_top_words.keys()):
        #     for jx, (author, tw) in enumerate(range(self.author_topics_weighted)):
        #         top_n_topics_author = self.author_topics_weighted[author]
        #         pass

        for i_x, (author, tw) in enumerate(self.author_topics_weighted.iteritems()):
            for t, _ in tw[:n_topics_per_author]:
                incidence_mat[i_x, t] = 1
        pass
        print

    def run(self):
        self.find_proper_authors()
        self.link_authors_papers_topics()
        self.create_topic_author_matrix()


def main():
    # my code here
    assoc_discover = DiscoverAssociations()
    assoc_discover.run()


if __name__ == "__main__":
    main()
