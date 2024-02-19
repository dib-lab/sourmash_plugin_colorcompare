"""xyz plugin description"""

usage="""
   sourmash scripts color_compare
"""

epilog="""
See https://github.com/xyz for more examples.

Need help? Have questions? Ask at http://github.com/sourmash-bio/sourmash/issues!
"""

import argparse

import scipy.cluster.hierarchy as sch
import pandas as pd
import numpy
import pylab
import seaborn as sns
from scipy.cluster.hierarchy import linkage

import sourmash
from sourmash.plugins import CommandLinePlugin

#
# CLI plugin - supports 'sourmash scripts color_compare'
#

class Command_ColorCompare(CommandLinePlugin):
    command = 'color_compare'             # 'scripts <command>'
    description = __doc__       # output with -h
    usage = usage               # output with no args/bad args as well as -h
    epilog = epilog             # output with -h
    formatter_class = argparse.RawTextHelpFormatter # do not reformat multiline

    def __init__(self, subparser):
        super().__init__(subparser)
        subparser.add_argument('compare_csv')
        subparser.add_argument('categories_csv')
        subparser.add_argument('-o', '--output', required=True)
                               
    def main(self, args):
        super().main(args)
        return color_compare(args.compare_csv,
                             args.categories_csv,
                             args.output)


def color_compare(compare_csv, categories_csv, output):
    # set font scale for sns
    sns.set(font_scale=0.1) 

    # set colors for each of the environments
    colours = {'ocean': 'blue', 
               'agsoil': 'brown', 
               'lake': 'yellow', 
               'peat': 'green',
              'natsoil': 'orange',
              'other': 'grey'}

    df= pd.read_csv(compare_csv, sep=',')

    # open the attributes for each sequence (in this case environment it comes from)
    attr = pd.read_csv(categories_csv, sep=',', index_col=0)

    # set index as colnames
    df.index = df.columns

    # add the labels to a list
    labeltext = df.index.to_list()
    dendrolabels = labeltext

    # Create dendrogram
    Y = sch.linkage(df, method='single')  # centroid
    Z1 = sch.dendrogram(Y, orientation='left', labels=dendrolabels, get_leaves=True)
    # re-order labels along rows, top to bottom
    idx1 = Z1['leaves']
    reordered_labels = [labeltext[i] for i in idx1 ]

    # reindex and reorder dataframe
    df = df.reindex(columns=reordered_labels, index=reordered_labels)

    # Add the index vales as labels to merge with attributes on label names
    df['label'] = df.index

    # merge with the attribute table
    df = pd.merge(df, attr, on='label')

    # make the index names the orignal label names instead of numbers
    df.index = df['label']

    # remove the extra label column
    del df['label']

    # add the colors for each of the labels
    row_colors = df['attr'].map(colours)
    g = sns.clustermap(data=df.drop(['attr'], axis=1, ), 
                       cmap="YlGnBu", row_colors=row_colors, row_cluster=True, col_cluster=False, 
                       dendrogram_ratio=0.05, method='single', cbar_pos=None)
    g.savefig(output, bbox_inches='tight')

    return 0
