# all tex related stuff is in src/tex.py
import numpy as np
import pylatex as pl
import pandas as pd
from marketwatch import split_tables
from utils.tex import plot_df_as_table


def main():
    df = pd.DataFrame({'a': [1,2,3], 'b': [9,8,7]})
    df.index.name = 'x'

    M = np.matrix(df.values)

    doc = pl.Document()

    doc.packages.append(pl.Package('booktabs'))
    doc.packages.append(pl.Package('adjustbox'))

    with doc.create(pl.Section('Matrix')):
        doc.append(pl.Math(data=[pl.Matrix(M)]))

    dfs, captions = split_tables()
    # MARKET EVENTS
    for index, df in enumerate(dfs):
        with doc.create(pl.Table(position='htbp')) as table:
            table.add_caption(captions[index])
            table.append(pl.Command('centering'))
            doc.append(pl.NoEscape(r'\begin{adjustbox}{width=1\textwidth}'))
            table.append(pl.NoEscape(df.to_latex(escape=True, index=False, column_format='lcccccc')))
            doc.append(pl.NoEscape(r'\end{adjustbox}'))


    # PULL REDDIT DATA

    doc.generate_tex('full')


if __name__ == '__main__':
    main()


# test_table = dfs[2]
# # trip Report column to 15 characters
# test_table["Report"] = test_table["Report"].str.slice(0, 25)
# plot_df_as_table(test_table)