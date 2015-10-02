# coding: utf-8
from collections import defaultdict
import itertools
from external_sources.test_gscholar import GetGScholarInfo

__author__ = 'Pavel Soriano'
__mail__ = 'sorianopavel@gmail.com'
import re

import logging
from sys import stdout

import pandas as pd
from utils import my_language_detect, get_texts

# from langdetect.detector_factory import PROFILES_DIRECTORY
# from langdetect import detect
# logging.basicConfig(filename='pavel_log.log', filemode='w', level=logging.INFO)
logging.basicConfig(stream=stdout, level=logging.INFO)


def load_data_egc(data_path):
    egc_df = pd.read_csv(data_path, sep="\t", error_bad_lines=False, encoding="utf-8")
    return egc_df


def pdf2txt(pdf_folder):
    from subprocess import call

    pdf_files = get_texts(pdf_folder, "pdf")

    for f in pdf_files:
        try:
            call("java -jar ../input/pdfs/pdfbox-app-1.8.5.jar ExtractText {0}".format(f), shell=True)
            logging.info("Extracted text from {}".format(f))
        except:
            logging.warning("Could not extract text from {}".format(f))
    pass


def download_pdfs(df, what_to_download="1page"):
    import urllib
    col_dict = {"1page": "pdf1page", "full": "pdfarticle"}
        # Download 1page pdfs
    logging.info("Downloading {} pdf files.".format(what_to_download))
    for f in df.iterrows():

        try:
            urllib.urlretrieve(f[1][col_dict[what_to_download]], "../input/pdfs/{}/".format(col_dict[what_to_download])
                               + str(f[1]['id']) + ".pdf")
            logging.info("Downloaded {}".format((f[1]['title']).encode('utf8')))
        except:
            logging.warning('Could not download {0}:{1}'.format(f[1]["id"], (f[1]['title']).encode('utf8')))
            filo = open("../input/pdfs/1page/{}_URL_INVALID.error".format(f[1]["id"]), "w")
            filo.close()
            #
            # if what_to_download == "full":
            #
            #     # Download full page pdfs
            #     logging.info("Downloading full pdf files.")
            #     for f in df.iterrows():
            #         try:
            #             urllib.urlretrieve(f[1]['pdfarticle'], "../input/pdfs/full/" + str(f[1]['id']) + ".pdf")
            #             logging.info("Downloaded {}".format((f[1]['title']).encode('utf8')))
            #         except:
            #             logging.warning('Could not download {0}:{1}'.format(f[1]["id"], (f[1]['title']).encode('utf8')))
            #             filo = open("../input/pdfs/full/{}_URL_INVALID.error".format(f[1]["id"]), "w")
            #             filo.close()


def add_new_columns(df):
    def add_abstract_plus_title(df):
        df["long_content"] = df["title"] + " " + df["abstract"].fillna("")
        return df

    def add_abstract_plus_title_lemmas(df):
        df["short_content"] = df["title"] + " " + df["abstract"].fillna("")
        return df

    def add_affiliations(df):
        list_affiliations = []
        for doc_id in df["id"].values:
            temp = get_doc_emails(doc_id)
            if isinstance(temp, list):
                temp = ", ".join(temp)
            list_affiliations.append(temp)
        df["affiliations"] = list_affiliations
        return df

    df = add_abstract_plus_title(df)
    df = add_affiliations(df)
    df = add_abstract_plus_title_lemmas(df)
    df.to_csv("../input/RNTI_articles_export_fixed1347_ids.txt", sep="\t", encoding="utf-8", index=False,
              index_label=False)

    return df

def add_index_column(df):
    df["id"] = range(0, len(df))
    df.to_csv("../input/RNTI_articles_export_fixed1347_ids.txt", sep="\t", encoding="utf-8", index=False,
              index_label=False)
    return df


def add_lang_column(df):
    from collections import Counter

    if "lang" in df.columns:
        del df["lang"]
    idx_with_abstract = [not b for b in df["abstract"].isnull().tolist()]

    # We dont need idx with title cause they all have title
    langs_title = [my_language_detect(l[1]['title']) for l in df.iterrows()]
    langs_abstract = [my_language_detect(l[1]['abstract']) for l in df.iloc[idx_with_abstract].iterrows()]

    print "Langs Title: ", Counter(langs_title)
    print "Langs Abstract: ", Counter(langs_abstract)

    df["lang_title"] = langs_title

    df["lang_abstract"] = ""
    df.loc[idx_with_abstract, "lang_abstract"] = langs_abstract

    df.to_csv("../input/RNTI_articles_export_fixed1347_ids.txt", sep="\t", encoding="utf-8", index=False,
              index_label=False)
    return df


def do_OCR(df, path_txt_files, min_size, list_files=None):
    """
    NEEDS imagemagick and tesseract-ocr
    :param df: I need the complete df to get the language cause the program that does the OCR needs the supposed language
    of the image
    :param path_txt_files:
    :param min_size:
    :return:
    """
    lang_map = {"en": "eng", "fr": "fra"}
    import os
    from subprocess import call

    if list_files:
        text_files = list_files
    else:
        text_files = get_texts(path_txt_files, "txt")

    for f in text_files:
        if os.path.getsize(f) < min_size or list_files:
            lang = df.loc[df["id"] == int(os.path.basename(f)[:-4])]["lang_title"].tolist()[0]
            call(
                "convert -density 300 {0}[0] -depth 8 -background white -alpha remove -flatten +matte  {0}.tiff".format(
                f.replace(".txt", ".pdf")), shell=True)
            call("tesseract -l {0} {1}.tiff {2}".format(lang_map[lang], f.replace(".txt", ".pdf"), f[:-4]), shell=True)
            call("rm {0}.tiff".format(f.replace(".txt", ".pdf")), shell=True)


def get_EGC_articles(df):
    return df[df["booktitle"] == "EGC"].copy()

def get_french_articles(df):
    return df[df["lang_title"] == "fr"].copy()



def detect_garbage_text(text_path, min_chars=2):
    import re

    garbage_files = []
    txt_files = get_texts(text_path, "txt")
    # txt_files = ["../input/pdfs/1page/1630.txt"]
    stop_words = set([l.strip("\n").decode("utf-8") for l in open("ngrams/stopwords.txt").readlines() if l])
    for t in txt_files:
        with open(t, "r") as f:
            content = f.read().replace("\n", "")
            search_re = "\w{{{min},}}".format(min=str(min_chars))
            words = re.findall(search_re, content)
            all_words = re.findall("\w+", content)
            if len(words) < 10 or len(stop_words.intersection(all_words)) < 5:
                logging.info("Garbage text!! File {}".format(t))
                logging.debug(content)
                garbage_files.append(t)
    return garbage_files

    pass


def getfull_pdfs(df):
    # Get pdfs from the interwebz
    download_pdfs(df, what_to_download="full")

    # Convert pdfs to txt
    pdf2txt("../input/pdfs/full")

    # Detect those pdfs that have garbage text and try to obtain the text through OCR
    gt = detect_garbage_text("../input/pdfs/full")

    if not gt:
        logging.info("Good. No garbage files.")

    # Do OCR on those detected as shitty text
    else:
        logging.info("Not good. We have garbage files.")
        do_OCR(df, "", 0, list_files=gt)


def get_doc_emails(doc_id):
    try:
        doc_text = open("../input/pdfs/1page/{}.txt".format(doc_id)).read()
    except:
        return []
    matcho = re.findall(r"@[A-Za-z0-9\._-]+\b", doc_text)
    return matcho
    pass
def get1page_pdfs(df):
    """
    Get the 1page pdfs for all the papers on df
    :param df:
    :return:
    """

    # 1. Get pdfs from the interwebz
    download_pdfs(df, what_to_download="1page")

    # 2. Convert pdfs to txt
    pdf2txt("../input/pdfs/1page")

    # 3. Do OCR to those pdfs that seem to be images. Do it with those text files smaller than 17bytes (
    do_OCR(df, "../input/pdfs/1page", 17)

    # 4. Detect those pdfs that have garbage text and try to obtain the text through OCR
    gt = detect_garbage_text("../input/pdfs/1page", 5)
    if not gt:
        logging.info("Good. No garbage files.")

    # 4.1 Do OCR on those detected as shitty text
    else:
        logging.info("Not good. We have garbage files.")
        do_OCR(df, "", 0, list_files=gt)


def add_citations_column():
    migs = GetGScholarInfo()
    migs.run()


def normalize_affiliations():
    df = load_data_egc("../input/RNTI_articles_export_fixed1347_ids.txt")
    df = get_EGC_articles(df)
    affiliations = df.affiliations.fillna("").values
    affiliations_new = [m.split(", ") for m in affiliations]
    affiliations_new = [m.lower() for m in list(itertools.chain.from_iterable(affiliations_new)) if len(m) > 5]
    normalized_affiliations = {}
    for j in affiliations_new:
        for k in affiliations_new:
            if j != k and j[1:] in k:
                normalized_affiliations[k] = j

    new_affiliations = []
    for m in affiliations:

        splito = m.split(", ")
        temp = []
        for s in splito:
            if "bat710" in s:
                pass
            if len(s) < 5:
                continue
            temp.append(normalized_affiliations.get(s.lower(), s.lower()))
        if not temp or not m:
            new_affiliations.append("")
        else:
            new_affiliations.append(", ".join(temp))

    df["affiliations"] = new_affiliations
    df.to_csv("../input/RNTI_articles_export_fixed1347_ids.txt", sep="\t", encoding="utf-8", index=False,
              index_label=False)
    return new_affiliations

def main():
    df = load_data_egc("../input/RNTI_articles_export_original.txt")
    df = get_EGC_articles(df)
    df = add_lang_column(df)
    df = get_french_articles(df)
    add_index_column(df)
    df = add_new_columns(df)
    normalize_affiliations()
    get1page_pdfs(df)
    getfull_pdfs(df)
    # df = get_EGC_articles(df)


if __name__ == "__main__":
    main()
