# all tex related stuff is in src/tex.py
import numpy as np
import pylatex as pl
import pandas as pd
from marketwatch import split_table, get_tables
from utils import plot_df_as_table

def make_report( report_data: dict, file_name = "full"):

    tables = report_data["tables"]
    doc = pl.Document()

    doc.packages.append(pl.Package('booktabs'))
    doc.packages.append(pl.Package('adjustbox'))

    dfs, captions = split_table(tables[0])
    # Difference to the other answer:

    # first table
    for index, df in enumerate(dfs):
        with doc.create(pl.Table(position='htbp')) as table:
            table.add_caption(captions[index])
            table.append(pl.Command('centering'))
            doc.append(pl.NoEscape(r'\begin{adjustbox}{width=1\textwidth}'))
            table.append(pl.NoEscape(df.to_latex(escape=True, index=False, column_format='lcccccc')))
            doc.append(pl.NoEscape(r'\end{adjustbox}'))

    # second table, next weeks events
    dfs, captions = split_table(tables[1])

    for index, df in enumerate(dfs):
        with doc.create(pl.Table(position='htbp')) as table:
            table.add_caption(captions[index])
            table.append(pl.Command('centering'))
            doc.append(pl.NoEscape(r'\begin{adjustbox}{width=1\textwidth}'))
            table.append(pl.NoEscape(df.to_latex(escape=True, index=False, column_format='lcccccc')))
            doc.append(pl.NoEscape(r'\end{adjustbox}'))

    doc.generate_tex(file_name)

# test_table = dfs[2]
# # trip Report column to 15 characters
# test_table["Report"] = test_table["Report"].str.slice(0, 25)
# plot_df_as_table(test_table)