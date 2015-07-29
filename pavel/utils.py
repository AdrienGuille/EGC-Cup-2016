from langdetect import DetectorFactory, PROFILES_DIRECTORY

__author__ = 'Pavel Soriano'
__mail__ = 'sorianopavel@gmail.com'

factory = DetectorFactory()
factory.load_profile(PROFILES_DIRECTORY)


def my_detect(text):
    detector = factory.create()
    detector.set_prior_map({"en": 0.1, "fr": .1})
    if not text:
        return
    detector.append(text)
    return detector.detect()


def get_files(folder_path, extension):
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
