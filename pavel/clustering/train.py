from __future__ import print_function
from collections import defaultdict

import numpy as np

from clustering.models import build_unsup_nmf_topics
from ngrams.utils import load_text_data

__author__ = 'Pavel Soriano'
__mail__ = 'sorianopavel@gmail.com'


def nmf_clustering(data, doc_topic_mat=None, topic_token_mat=None, feature_names=None, k=15):
    n_words_per_topic = 20
    n_docs_per_topic = 30
    n_topics_per_doc = 20
    if not doc_topic_mat:
        nmf = build_unsup_nmf_topics(n_topics=k)
        doc_topic_mat = nmf.fit_transform(data.values())
        feature_names = nmf.named_steps["vectorize"].get_feature_names()
        topic_token_mat = nmf.named_steps["clust"].components_

    dict_topic_top_words = defaultdict(list)
    dict_topic_top_docs = defaultdict(list)
    for topic_idx, topic in enumerate(topic_token_mat):
        print("Topic #%d:" % topic_idx)
        # print(" ".join([feature_names[i] for i in topic.argsort()[:-10:-1]]))
        line = ""
        for i in topic.argsort()[:-n_words_per_topic + 1:-1]:
            term = "".join(feature_names[i])
            line += term
            line += " | "
            dict_topic_top_words[int(topic_idx)].append(term)
        print(line)
    dict_doc_top_topics = {}

    doc_orig_ids = np.array(data.keys())
    for topic_idx, topic in enumerate(np.transpose(doc_topic_mat)):
        dict_topic_top_docs[int(topic_idx)].extend(doc_orig_ids[topic.argsort()[:-n_docs_per_topic + 1:-1]])
        # print (topic[topic.argsort()[:-30:-1]])
    for idx, doc_id in enumerate(data.keys()):
        # dict_doc_top_topics[doc_id].extend(doc_topic_mat[idx, :].argsort()[::-1][:n_topics_per_doc])
        sorted_vals = doc_topic_mat[idx, :].argsort()[::-1][:n_topics_per_doc]
        dict_doc_top_topics[int(doc_id)] = zip(sorted_vals, doc_topic_mat[idx, :][sorted_vals])

    return dict_topic_top_words, dict_doc_top_topics, dict_topic_top_docs


def run_models():
    one_pages = load_text_data("../../input/pdfs/1page/", "txt")
    dict_topic_top_words, dict_doc_top_topics = nmf_clustering(one_pages)


def main():
    run_models()


if __name__ == "__main__":
    main()
