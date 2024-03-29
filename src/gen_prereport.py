import sys

# all tex related stuff is in src/tex.py
import numpy as np
import pylatex as pl
import pandas as pd
import datetime
from marketwatch import split_tables
from utils.parse_reddit import fetch_reddit_posts, parse_reddit_posts, make_dirs
from utils.tex import escape_latex
from utils.openbb_data import openbb_economy

def main():

    doc = pl.Document()

    doc.packages.append(pl.Package('booktabs'))
    doc.packages.append(pl.Package('adjustbox'))
    doc.packages.append(pl.Package("hyperref"))

    dfs, captions = split_tables()
    # MARKET EVENTS
    for index, df in enumerate(dfs):
        # only add these ta
        try:
            column_format = 'l' + 'c' * (len(df.columns) - 1)
            tex_table = df.to_latex(escape=True, index=False, column_format=column_format)
            with doc.create(pl.Table(position='htbp')) as table:
                table.add_caption(captions[index])
                table.append(pl.Command('centering'))
                doc.append(pl.NoEscape(r'\begin{adjustbox}{width=1\textwidth}'))
                table.append(pl.NoEscape(tex_table))
                doc.append(pl.NoEscape(r'\end{adjustbox}'))
        except Exception as e:
            print(e)
    # PULL REDDIT DATA
    # TODO integrate custom commands
    # eventually https://jeltef.github.io/PyLaTeX/current/examples/own_commands_ex.html
    reddit_posts = fetch_reddit_posts()
    # eventually do a md framed component per post
    if reddit_posts is not None and len(reddit_posts) > 0:
        df_posts = parse_reddit_posts(reddit_posts)
        # add reddit post to tex report
        with doc.create(pl.Itemize()) as itemize:
            for index, row in df_posts.iterrows():
                itemize.add_item(pl.NoEscape(r"\href{" + escape_latex(row['url']) + r"}{" + escape_latex(row['title']) + r"}," + escape_latex(row["linkFlairText"])))
        # with doc.create(pl.Table(position='htbp')) as table:
        #     table.append(pl.Command('centering'))
        #     doc.append(pl.NoEscape(r'\begin{adjustbox}{width=1\textwidth}'))
        #     # probably make some smartbox or text post instead.
        #     # In future versions `DataFrame.to_latex` is expected to utilise the base implementation of `Styler.to_latex` for formatting and rendering. The arguments signature may therefore change. It is recommended instead to use `DataFrame.style.to_latex` which also contains additional functionality.
        #     table.append(pl.NoEscape(df_posts.to_latex(escape=False, index=False, columns=['title', 'url', 'linkFlairText']))) 
        #     doc.append(pl.NoEscape(r'\end{adjustbox}'))
    economy_dfs, file_names = openbb_economy()
    for index, df in enumerate(economy_dfs):
        tex_table = df.to_latex(escape=True, index=False)
        with doc.create(pl.Table(position='htbp')) as table:
            table.add_caption(file_names[index])
            table.append(pl.Command('centering'))
            doc.append(pl.NoEscape(r'\begin{adjustbox}{width=1\textwidth}'))
            table.append(pl.NoEscape(tex_table))
            doc.append(pl.NoEscape(r'\end{adjustbox}'))
    # make images
    # make dirs files
    curr_month = datetime.datetime.now().strftime("%B")
    base_folder = f"data/reports/{curr_month}"
    make_dirs(base_folder)
    output_path = f"{base_folder}/report_{datetime.datetime.now().strftime('%Y_%m_%d')}_pre"
    doc.generate_tex(output_path)
    doc.generate_tex("data/latest")

if __name__ == '__main__':
    main()
