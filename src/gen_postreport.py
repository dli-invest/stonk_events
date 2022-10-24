import sys

# all tex related stuff is in src/tex.py
import numpy as np
import pylatex as pl
import pandas as pd
import datetime
from marketwatch import split_tables
from utils.parse_reddit import fetch_reddit_posts, parse_reddit_posts, make_dirs
from utils.tex import escape_latex
from utils.summarize_text import summarize_text, ensure_punkt_installed

def main():

    doc = pl.Document()
    doc.preamble.append(pl.Command('title', 'Post Market Report'))
    doc.preamble.append(pl.Command('author', 'FriendlyUser'))
    doc.preamble.append(pl.Command('date', pl.NoEscape(r'\today')))

    doc.packages.append(pl.Package('booktabs'))
    doc.packages.append(pl.Package('adjustbox'))
    doc.packages.append(pl.Package("hyperref"))
    ensure_punkt_installed()


    # grab content from today's csv file
    # https://raw.githubusercontent.com/dli-invest/fdrtt-stream/main/data/Bloomberg/2022-10/bloomberg_23.csv
    # get date in YYYY-MM format

    rel_date = datetime.datetime.now().strftime("%Y-%m")
    # get current day number 
    day = datetime.datetime.now().strftime("%d")
    file_to_access = f"https://raw.githubusercontent.com/dli-invest/fdrtt-stream/main/data/Bloomberg/{rel_date}/bloomberg_{day}.csv"

    # load file as csv 
    try:
        df = pd.read_csv(file_to_access)
    except Exception as e:
        print(e)
        df = pd.DataFrame()

    text_to_analyze = []
    # iterate across text and then use sumpy to summarize
    for index, row in df.iterrows():
        # add text to doc
        text_to_analyze.append(row['text'])
        if index % 12 == 0:
            raw_text = " ".join(text_to_analyze)
            summary = summarize_text(raw_text)
            # read current date from row["created_at"] and format as HH:MM:SS
            current_date = datetime.datetime.strptime(row["created_at"], "%Y-%m-%d %H:%M:%S").strftime("%H:%M:%S")
            doc.append(pl.utils.bold(current_date))
            doc.append(pl.basic.NewLine())
            doc.append(pl.escape_latex(summary))
            # summarize text
            # add summary to doc
            # clear text_to_analyze
            text_to_analyze = []
        # add summary to doc


    curr_month = datetime.datetime.now().strftime("%B")
    base_folder = f"data/reports/{curr_month}"
    make_dirs(base_folder)
    output_path = f"{base_folder}/report_{datetime.datetime.now().strftime('%Y_%m_%d')}_post"
    doc.generate_tex(output_path)
    doc.generate_tex("data/latest")

if __name__ == '__main__':
    main()
