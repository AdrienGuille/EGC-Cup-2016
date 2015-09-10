from __future__ import print_function
from clustering.models import build_unsup_nmf
from ngrams.utils import load_data

__author__ = 'Pavel Soriano'
__mail__ = 'sorianopavel@gmail.com'


def eval_models():
    one_pages = load_data("../../input/pdfs/1page/", "txt")
    nmf = build_unsup_nmf()
    result = nmf.fit(one_pages.values())
    feature_names = result.named_steps["vectorize"].get_feature_names()
    components = result.named_steps["clust"].components_
    for topic_idx, topic in enumerate(components):
        print("Topic #%d:" % topic_idx)
        # print(" ".join([feature_names[i] for i in topic.argsort()[:-10:-1]]))
        line = ""
        for i in topic.argsort()[:-10:-1]:
            line += "".join(feature_names[i]) + " | "
        print(line)

    print()
    pass


def main():
    eval_models()


if __name__ == "__main__":
    main()
