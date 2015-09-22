from collections import defaultdict
from clustering.train import nmf_clustering
from ngrams.utils import load_text_data

__author__ = 'Pavel Soriano'
__mail__ = 'sorianopavel@gmail.com'


def generate_nmf_json():
    one_pages = load_text_data("../../input/pdfs/1page/", "txt")
    dict_topics = nmf_clustering(one_pages)
    d3js_dict = defaultdict(list)

    print "jaja"
    pass


def main():
    # my code here
    generate_nmf_json()


if __name__ == "__main__":
    main()
