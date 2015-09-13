from __future__ import print_function
from collections import defaultdict
from clustering.models import build_unsup_nmf
from ngrams.utils import load_data

__author__ = 'Pavel Soriano'
__mail__ = 'sorianopavel@gmail.com'


def nmf_clustering(data):
    nmf = build_unsup_nmf()
    result = nmf.fit_transform(data.values())
    # H = nmf.transform()
    feature_names = nmf.named_steps["vectorize"].get_feature_names()
    components = nmf.named_steps["clust"].components_

    dict_topics = defaultdict(list)
    for topic_idx, topic in enumerate(components):

        print("Topic #%d:" % topic_idx)
        # print(" ".join([feature_names[i] for i in topic.argsort()[:-10:-1]]))
        line = ""
        for i in topic.argsort()[:-10:-1]:
            term = "".join(feature_names[i])
            line += term
            line += " | "
            dict_topics[topic_idx].append(term)
        print(line)
    return dict_topics


def run_models():
    one_pages = load_data("../../input/pdfs/1page/", "txt")
    nmf_clustering(one_pages)


def main():
    run_models()


if __name__ == "__main__":
    main()
