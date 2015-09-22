# coding: utf-8
from collections import defaultdict, Counter
import itertools
from clustering.models import build_unsup_nmf_locations
from data_manips import get_EGC_articles, load_data_egc
from external_sources.spotlight_access import get_spotlight_annotation
from ngrams.utils import load_text_data
from utils import dict_to_csv
import numpy as np
__author__ = 'Pavel Soriano'
__mail__ = 'sorianopavel@gmail.com'


def get_location_spotlight(n_lines=10):
    """
    Gets the location according to dbpedia spotlight from the first 10 lines of the 1page pdfs. Or the first n lines
    until "resume" is found.
    :return:
    """

    def filter_locations(list_annotations):

        filtered_list = []
        dbpedia_types = ["Place", "Education"]
        for v in list_annotations:
            if any([t for t in dbpedia_types if t in v["types"]]):
                filtered_list.append(v)
        return filtered_list

    # egc_df = get_EGC_articles(load_data_egc("../../input/RNTI_articles_export_fixed1347_ids.txt"))
    one_pages = load_text_data("../../input/pdfs/1page/", "txt")
    dict_locations = defaultdict(list)
    for page_idx, doc in one_pages.iteritems():
        first_lines = [l.lower() for l in doc.split("\n")[:n_lines]]
        resume_in = [True if u"résumé" in t else False for t in first_lines]
        if any(resume_in):
            first_lines = first_lines[:resume_in.index(True)]
        text = " ".join(first_lines)
        result = get_spotlight_annotation(text)
        if not result:
            continue
        result = filter_locations(result)
        dict_locations[page_idx].extend(list(set([r["surfaceForm"] for r in result])))
        print page_idx
    import pandas
    df = pandas.DataFrame(dict_locations.items(), columns=["id", "1page_location"])
    df.to_csv("../../input/location_1pagePDF.csv", index_label=False, index=False)


def get_location_rulebased():
    import re
    asterisks = [u"*", u"\u2217", u""]
    abstracts = [u"mmary", u"bstract", u"ésumé"]

    def treat_no_asterisks(text_list, authors):
        authors = [s for n in authors for s in n.split() if len(s) > 2]
        possible_location = ur"(niversi[dt])|(\b[A-Z]{3,}[0-9]?\b)|(aborato)|([rR]&[dD])|(cherche)|(esearch)|(Labs)|" \
                            ur"(Ecole)|(Tech)|(part[.]?ment)"
        locaion_list = []
        for l in text_list:
            # if we have already the email addres, we go to the next document
            if "@" in l or " AT " in l:
                break
            # if author names in line, we continue to next line
            if any([n in l.lower() for n in authors]):
                continue
            # if we are already on the abstracts we go to next document
            if any([a in l for a in abstracts]):
                break
            # finally, if we found one of the possible location markers, we keep the line
            findo = re.findall(possible_location, l)
            if findo:
                locaion_list.append(l)
        return locaion_list

    def treat_asteriks(text_list, asterisks_idx):

        asterisks_idx = np.array(asterisks_idx)
        text_list = np.array(text_list)
        lines_with_asterisk = [re.sub(ur"[\u2217\*]+", "", l, re.UNICODE) for l in text_list[asterisks_idx]]

        return lines_with_asterisk

    egc_df = get_EGC_articles(load_data_egc("../../input/RNTI_articles_export_fixed1347_ids.txt"))
    one_pages = load_text_data("../../input/pdfs/1page/", "txt")
    locations_dict = defaultdict(list)
    for page_idx, doc in one_pages.iteritems():
        authors = [n.lower() for n in egc_df[egc_df["id"] == int(page_idx)]["authors"].values[0].split(",")]
        doc_split = [l for l in doc.split("\n") if len(l.strip()) > 2]
        first_lines = [l for l in doc_split[2:10]]
        text_lines = "\n".join(first_lines)
        # if u"*" in text_lines or u"\u2217" in text_lines:
        asterisk_idx = [True if l[0] in asterisks else False for l in first_lines]
        if any(asterisk_idx):
            info_location = treat_asteriks(first_lines, asterisk_idx)
            # print info_location
            # print
            # print text_lines
            # print "***"*80
            # with_stars+=1
        else:
            # print "---"*80
            info_location = treat_no_asterisks(first_lines, authors)

        locations_dict[page_idx].extend(info_location)

    dict_to_csv("../../input/location_1pageRB.csv", locations_dict, columns=["id", "location"])
    # print "From {0} 1page pdf, {1} have stars in first lines".format(len(one_pages), with_stars)

    return locations_dict


def clean_list(noisy_list):
    noise = [u"@"]
    noisy_list = [n.strip().lstrip().lower() for n in noisy_list if n]
    noisy_elements = np.array([False if l in n else True for l in noise for n in noisy_list], dtype=np.bool)
    noisy_list = np.array(noisy_list)

    return noisy_list[noisy_elements]


def similarity_locations(locations_dict):
    merged = list(set(itertools.chain.from_iterable(locations_dict.values())))
    merged = clean_list(merged).tolist()
    dict_substrings = defaultdict(dict)
    list_subs = []
    for i in range(len(merged)):
        for j in range(i + 1, len(merged) - 1):
            substring = longest_common_substring(merged[i].replace(" ", "__"), merged[j].replace(" ", "__"))
            if len(substring) > 3:
                list_subs.append(substring)
            dict_substrings[merged[0]][merged[1]] = substring
    histo = Counter(list_subs)
    print histo


def longest_common_substring(s1, s2):
    m = [[0] * (1 + len(s2)) for i in xrange(1 + len(s1))]
    longest, x_longest = 0, 0
    for x in xrange(1, 1 + len(s1)):
        for y in xrange(1, 1 + len(s2)):
            if s1[x - 1] == s2[y - 1]:
                m[x][y] = m[x - 1][y - 1] + 1
                if m[x][y] > longest:
                    longest = m[x][y]
                    x_longest = x
            else:
                m[x][y] = 0
    return s1[x_longest - longest: x_longest]


def cluster_locations(dict_locations):
    nmf = build_unsup_nmf_locations()
    # result = nmf.fit_transform(list(itertools.chain.from_iterable(dict_locations.values())))
    result = nmf.fit_transform([" ".join(v) for v in dict_locations.values()])

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
    pass


def main():

    # my code here
    print
    locations = get_location_rulebased()
    cluster_locations(locations)
    # similarity_locations(locations)
    # get_location_spotlight()


if __name__ == "__main__":
    main()
