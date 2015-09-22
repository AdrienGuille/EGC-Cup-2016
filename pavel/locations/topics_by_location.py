from collections import defaultdict, Counter
import itertools
from clustering.train import nmf_clustering
from data_manips import get_EGC_articles
from data_manips import load_data_egc
from ngrams.utils import load_text_data
import re
import pandas as pd

__author__ = 'Pavel Soriano'
__mail__ = 'sorianopavel@gmail.com'


def get_abstract_and_title_topics():
    egc_df = get_EGC_articles(load_data_egc("../../input/RNTI_articles_export_fixed1347_ids.txt"))

    egc_df["title+abstract"] = egc_df["title"] + " " + egc_df["abstract"].fillna("")
    data = dict(zip(egc_df["id"].tolist(), egc_df["title+abstract"].tolist()))
    return nmf_clustering(data, k=15)


def get_1page_topics():
    one_pages = load_text_data("../../input/pdfs/1page/", "txt")
    return nmf_clustering(one_pages)


def normalize_mails(dict_author_affiliation):
    list_mails = list(itertools.chain.from_iterable(dict_author_affiliation.values()))
    list_mails = [l for l in list(set(list_mails)) if l]
    dict_mail_normalize = defaultdict(list)
    for l in list_mails:
        for i in list_mails:
            if i != l and l[1:] in i:  # fuzz.token_sort_ratio(i, l) >= 75:
                dict_mail_normalize[i].append(l)
    normalized_dict_author_affiliation = defaultdict(list)
    for k, v in dict_author_affiliation.iteritems():
        for email in v:
            if email in dict_mail_normalize:
                normalized_dict_author_affiliation[k].extend(dict_mail_normalize[email])
            else:
                normalized_dict_author_affiliation[k].extend([email])
    return normalized_dict_author_affiliation


def load_ciprian_affiliations(path):
    import codecs
    import re
    arrobas = re.compile(r"@")
    dict_author_affiliation = defaultdict(list)
    file_lines = [l.strip().lstrip() for l in codecs.open(path, encoding="utf-8").readlines() if l]
    for l in file_lines:
        current_line = l.replace("[", "")
        current_line = current_line.replace("]", "")
        line_split = current_line.split(";")
        author_name = line_split[0].strip()
        author_affiliations = [f.strip().lstrip() for f in line_split[2].split(",") if line_split[2]]
        if not author_affiliations or not author_affiliations[0]:
            continue
        clean_affiliations = []

        for affi in author_affiliations:
            arr_split = affi.split("@")
            if len(arr_split) > 2:
                temp = ["@" + f for f in arr_split[1:]]
                clean_affiliations.extend(temp)
            else:
                clean_affiliations.append(affi)
        author_affiliations = list(set(clean_affiliations))
        dict_author_affiliation[author_name].extend(author_affiliations)
    dict_author_affiliation = normalize_mails(dict_author_affiliation)
    return dict_author_affiliation


def get_document_affiliation(author_affiliations, authors):
    # individual_authors = [a.strip().lstrip() for a in authors.split(",")]
    affiliations = []
    for f in authors:
        if f in author_affiliations:
            affiliations.extend(author_affiliations[f])
        else:
            pass
            # print "{} was not found in the dict author-affiliation. Not cool".format(f.encode("utf-8"))
    return affiliations


def get_doc_emails(doc_id):
    try:
        doc_text = open("../../input/pdfs/1page/{}.txt".format(doc_id)).read()
    except:
        return []
    matcho = re.findall(r"@[A-Za-z0-9\._-]+\b", doc_text)
    return matcho
    pass


def load_doc_affiliations(df):
    dict_mails = defaultdict(list)
    for doc_id in df["id"]:
        mails = list(set(get_doc_emails(doc_id)))
        if mails:
            dict_mails[doc_id].extend(mails)
    normalized_mails = {}
    for i in dict_mails.values():
        for j in i:
            for k in i:
                if j != k and j[1:] in k:
                    normalized_mails[k] = j
    normalized_doc_mails = defaultdict(list)
    for doc_id, affils in dict_mails.iteritems():
        temp = []
        for m in affils:
            if not m:
                continue
            if m in normalized_mails:
                temp.append(normalized_mails[m])
            else:
                temp.append(m)
        normalized_doc_mails[doc_id].extend(temp)
    return normalized_doc_mails

    pass


def get_affiliation_topics(topics_func):
    # EGC data
    egc_df = get_EGC_articles(load_data_egc("../../input/RNTI_articles_export_fixed1347_ids.txt"))
    # Topics
    dict_topic_top_words, dict_doc_top_topics, dict_topic_top_docs = topics_func()
    # Affiliations
    dict_author_affiliations = load_ciprian_affiliations("../../ciprian/output/authors_email_affiliation.csv")
    dict_doc_affiliations = load_doc_affiliations(egc_df)

    dict_affiliation_top_topics = defaultdict(list)
    non_mails = 0
    for doc_id, topics_ids in dict_doc_top_topics.iteritems():
        doc_affiliations = dict_doc_affiliations[doc_id]
        if not doc_affiliations:
            doc_authors = [a.lstrip().strip() for a in
                           egc_df[egc_df["id"] == int(doc_id)]["authors"].values[0].lower().split(",")]
            doc_affiliations = get_document_affiliation(dict_author_affiliations, doc_authors)
        if not doc_affiliations:
            non_mails += 1
            continue
        doc_topics = dict_doc_top_topics[doc_id]

        for affi in doc_affiliations:
            dict_affiliation_top_topics[affi].append(doc_topics)
    print "There are {0} docs from {1} with no emails available".format(non_mails, len(dict_doc_top_topics))

    dict_topics_top_affiliations = {}
    for topic_id, top_docs in dict_topic_top_docs.iteritems():
        temp_affiliations = []
        for doc_id in top_docs:
            doc_affiliations = dict_doc_affiliations[doc_id]
            if not doc_affiliations:
                doc_authors = [a.lstrip().strip()
                               for a in egc_df[egc_df["id"] == int(doc_id)]["authors"].values[0].lower().split(",")]
                doc_affiliations = get_document_affiliation(dict_author_affiliations, doc_authors)
            if not doc_affiliations:
                continue
            temp_affiliations.extend(doc_affiliations)
        dict_topics_top_affiliations[topic_id] = Counter(temp_affiliations).most_common(5)

    pass


def main():
    # my code here
    get_affiliation_topics(get_abstract_and_title_topics)
    # get_abstract_and_title_topics()


if __name__ == "__main__":
    main()
