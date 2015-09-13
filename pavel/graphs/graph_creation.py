from collections import defaultdict
from clustering.train import nmf_clustering
from ngrams.utils import load_data

__author__ = 'Pavel Soriano'
__mail__ = 'sorianopavel@gmail.com'


def create_nmf_graph():
    one_pages = load_data("../../input/pdfs/1page/", "txt")
    dict_topics = nmf_clustering(one_pages)
    import pprint
    pprint.pprint(dict_topics)
    d3js_dict = defaultdict(list)
    # import snap as sn
    # G = sn.TUNGraph.New()
    # for topic_idx, topic in dict_topics.iteritems():


    pass


def main():
    create_nmf_graph()


if __name__ == "__main__":
    main()
