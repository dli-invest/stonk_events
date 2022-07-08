import numpy as np
import pylatex as pl
import pandas as pd
from extract_calendar_events import split_tables

df = pd.DataFrame({'a': [1,2,3], 'b': [9,8,7]})
df.index.name = 'x'

M = np.matrix(df.values)

doc = pl.Document()

doc.packages.append(pl.Package('booktabs'))
doc.packages.append(pl.Package('adjustbox'))

with doc.create(pl.Section('Matrix')):
    doc.append(pl.Math(data=[pl.Matrix(M)]))

dfs, captions = split_tables()
# Difference to the other answer:

for index, df in enumerate(dfs):
    with doc.create(pl.Table(position='htbp')) as table:
        table.add_caption(captions[index])
        table.append(pl.Command('centering'))
        doc.append(pl.NoEscape(r'\begin{adjustbox}{width=1\textwidth}'))
        table.append(pl.NoEscape(df.to_latex(escape=True, index=False, column_format='lcccccc')))
        doc.append(pl.NoEscape(r'\end{adjustbox}'))

doc.generate_tex('full')