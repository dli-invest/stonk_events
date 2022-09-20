# all tex related stuff is in src/tex.py
import numpy as np
import pylatex as pl
import pandas as pd
import datetime
from marketwatch import split_tables
from utils.parse_reddit import fetch_reddit_posts, parse_reddit_posts, make_dirs

def main():

    doc = pl.Document()

    doc.packages.append(pl.Package('booktabs'))
    doc.packages.append(pl.Package('adjustbox'))

    dfs, captions = split_tables()
    # MARKET EVENTS
    for index, df in enumerate(dfs):
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
            pass


    # PULL REDDIT DATA
    # TODO integrate custom commands
    # eventually https://jeltef.github.io/PyLaTeX/current/examples/own_commands_ex.html
    reddit_posts = fetch_reddit_posts()
    if reddit_posts is not None and len(reddit_posts) > 0:
        df_posts = parse_reddit_posts(reddit_posts)
        # add reddit post to tex report
        with doc.create(pl.Section('Reddit Posts')):
            with doc.create(pl.Table(position='htbp')) as table:
                table.append(pl.Command('centering'))
                doc.append(pl.NoEscape(r'\begin{adjustbox}{width=1\textwidth}'))
                # probably make some smartbox or text post instead.
                table.append(pl.NoEscape(df_posts.to_latex(escape=True, index=False, columns=['title', 'url', 'linkFlairText'])))
                doc.append(pl.NoEscape(r'\end{adjustbox}'))

    # make dirs files
    curr_month = datetime.datetime.now().strftime("%B")
    base_folder = f"../data/reports/{curr_month}"
    make_dirs(base_folder)
    output_path = f"{base_folder}/report_{datetime.datetime.now().strftime('%Y_%m_%d')}_pre"
    doc.generate_tex(output_path)
    doc.generate_tex("../data/latest")

if __name__ == '__main__':
    main()
