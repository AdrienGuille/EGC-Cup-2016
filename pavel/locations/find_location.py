# coding: utf-8
from collections import defaultdict
from data_manips import get_EGC_articles, load_data_egc
from external_sources.spotlight_access import get_spotlight_annotation
from ngrams.utils import load_data
from utils import dict_to_csv

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
    one_pages = load_data("../../input/pdfs/1page/", "txt")
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
        found_info = False
        possible_location = ur"(niversi[dt])|(\b[A-Z]{3,}[0-9]?\b)|(aborato)|([rR]&[dD])|(cherche)|(esearch)|(Labs)|" \
                            ur"(Ecole)|(Tech)|(part[.]?ment)"
        locaion_list = []
        for l in text_list:
            # if we have already the email addres, we go to the next document
            if "@" in l:
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
        import numpy as np

        asterisks_idx = np.array(asterisks_idx)
        text_list = np.array(text_list)
        lines_with_asterisk = [re.sub(ur"[\u2217\*]+", "", l, re.UNICODE) for l in text_list[asterisks_idx]]

        return lines_with_asterisk

    egc_df = get_EGC_articles(load_data_egc("../../input/RNTI_articles_export_fixed1347_ids.txt"))
    one_pages = load_data("../../input/pdfs/1page/", "txt")
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
    dict_to_csv("../../input/location_1pageRB.csv", locations_dict, ["id", "location"])
    # print "From {0} 1page pdf, {1} have stars in first lines".format(len(one_pages), with_stars)


def main():
    # my code here
    print
    get_location_rulebased()
    # get_location_spotlight()


if __name__ == "__main__":
    main()
