import math

__author__ = 'Pavel Soriano'
__mail__ = 'sorianopavel@gmail.com'

import logging

import pandas as pd
from utils import get_files, my_detect
from langdetect.detector_factory import PROFILES_DIRECTORY
from langdetect import detect
logging.basicConfig(filename='pavel_log.log', filemode='w', level=logging.INFO)


def load_data(data_path):
    egc_df = pd.read_csv(data_path, sep="\t", error_bad_lines=False, encoding="utf-8")
    return egc_df


def pdf2txt(pdf_folder):
    from subprocess import call
    pdf_files = get_files(pdf_folder, "pdf")

    for f in pdf_files:
        try:
            call("java -jar ../input/pdfs/pdfbox-app-1.8.5.jar ExtractText {0}".format(f), shell=True)
            logging.info("Extracted text from {}".format(f))
        except:
            logging.warning("Could not extract text from {}".format(f))
    pass


def download_pdfs(df):
    import urllib

    # Download 1page pdfs
    for f in df.iterrows():
        try:
            urllib.urlretrieve(f[1]['pdf1page'], "../input/pdfs/1page/" + str(f[1]['id']) + ".pdf")
            logging.info("Downloaded {}".format((f[1]['title']).encode('utf8')))
        except:
            logging.warning('Could not download {}'.format((f[1]['title']).encode('utf8')))

    # Download full page pdfs
    for f in df.iterrows():
        try:
            urllib.urlretrieve(f[1]['pdfarticle'], "../input/pdfs/full/" + str(f[1]['id']) + ".pdf")
            logging.info("Downloaded {}".format((f[1]['title']).encode('utf8')))
        except:
            logging.warning('Could not download {}'.format((f[1]['title']).encode('utf8')))



def add_index_column(df):
    df["id"] = range(0, len(df))
    df.to_csv("../input/RNTI_articles_export_fixed1347_ids.txt", sep="\t", encoding="utf-8", index=False, index_label=False)
    return df

def add_lang_column(df):
    from collections import Counter
    langs = [my_detect(l[1]['title']) for l in df.iterrows()]
    print Counter(langs)
    df["lang"] = langs

    df.to_csv("../input/RNTI_articles_export_fixed1347_ids.txt", sep="\t", encoding="utf-8", index=False, index_label=False)
    return df


def do_OCR(df, path_txt_files, min_size):
    lang_map = {"en":"eng", "fr":"fra"}
    import os
    from subprocess import call
    text_files = get_files(path_txt_files, "txt")
    for f in text_files:
        if os.path.getsize(f) < min_size:
            lang = df.loc[df["id"] == int(os.path.basename(f)[:-4])]["lang"].tolist()[0]
            call("convert -density 300 {0}[0] -depth 8 -background white -alpha remove  {0}.tiff".format(f.replace(".txt", ".pdf")), shell=True)
            call("tesseract -l {0} {1}.tiff {2}".format(lang_map[lang], f.replace(".txt", ".pdf"), f[:-4]), shell=True)
            call("rm {0}.tiff".format(f.replace(".txt", ".pdf")), shell=True)


def main():
    df = load_data("../input/RNTI_articles_export_original2.txt")
    # download_pdfs(df)
    # pdf2txt("../input/pdfs/1page")
    # pdf2txt("../input/pdfs/full")
    # add_index_column(df)
    df = add_lang_column(df)
    # do_OCR(df, "../input/pdfs/full", 3000)
    # do_OCR(df, "../input/pdfs/1page", 1000)
    pass
if __name__ == "__main__":
    main()