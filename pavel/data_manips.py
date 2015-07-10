__author__ = 'Pavel Soriano'
__mail__ = 'sorianopavel@gmail.com'

import logging

import pandas as pd
from utils import get_files

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
    df["id"] = range(1, len(df) + 1)
    df.to_csv("../input/RNTI_articles_export_fixed1347_ids.txt", sep="\t", encoding="utf-8")





def main():
    df = load_data("../input/RNTI_articles_export_fixed1347_ids.txt")
    download_pdfs(df)
    pdf2txt("../input/pdfs/1page")
    pdf2txt("../input/pdfs/full")

if __name__ == "__main__":
    main()