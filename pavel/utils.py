__author__ = 'Pavel Soriano'
__mail__ = 'sorianopavel@gmail.com'


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
