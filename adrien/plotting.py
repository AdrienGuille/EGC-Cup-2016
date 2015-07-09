# coding: utf-8
__author__ = "Adrien Guille"
__email__ = "adrien.guille@univ-lyon2.fr"

import matplotlib.pyplot as plt

def scatter_plot(data_x=None, data_y=[], plot_name='', file_path='output/default_plot.png', ymax=None, xmax=None, loglog=False):
    plt.clf()
    if ymax is not None:
        plt.ylim((0, ymax))
    if xmax is not None:
        plt.xlim((0, xmax))
    if data_x is None:
        if loglog:
            plt.loglog(data_y, marker='o', ls='')
        else:
            plt.plot(data_y, marker='o', ls='')
    else:
        if loglog:
            plt.loglog(data_x, data_y, marker='o', ls='')
        else:
            plt.plot(data_x, data_y, marker='o', ls='')
    plt.title(plot_name)
    plt.ylabel('y')
    plt.xlabel('x')
    plt.savefig(file_path)
