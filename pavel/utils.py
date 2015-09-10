from langdetect import DetectorFactory, PROFILES_DIRECTORY

__author__ = 'Pavel Soriano'
__mail__ = 'sorianopavel@gmail.com'

factory = DetectorFactory()
factory.load_profile(PROFILES_DIRECTORY)
reg_words = r'''(?x)
      \d+(\.\d+)?\s*%   # les pourcentages
    | 's                # l'appartenance anglaise 's
    | \w'               # les contractions d', l', j', t', s'
    '''
reg_words += u"| \w\u2019"  # version unicode
reg_words += u"|\w+|[^\w\s]"  # avec les antislashs




def my_detect(text):
    detector = factory.create()
    detector.set_prior_map({"en": 0.1, "fr": .1})
    if not text:
        return
    detector.append(text)
    return detector.detect()


def load_french_lexicon():
    from adrien.python.lexicon import load
    return load('../../input/OLDlexique.txt')


fr_lexicon = load_french_lexicon()


def french_tokenizer(text):
    from nltk import RegexpTokenizer
    tokenizer = RegexpTokenizer(r"(?u)\b\w\w+\b")
    toks = tokenizer.tokenize(text)
    # We also lemmatize!
    # toks = [fr_lexicon.get(t, t) for t in toks]
    return toks


def get_texts(folder_path, extension):
    """
    Get the file names of all files inside 'folder_path'
    """
    import os, os.path
    # if os.path.isabs(folder_path):
    #     path_to_use = folder_path
    # else:
    #     path_to_use = os.getcwd() + folder_path
    listing = []
    for root, dirs, files in os.walk(folder_path):
        for f in files:
            if extension in f[-3:]:
                listing.append(os.path.join(root, f))

    return listing
