# parse reddit data resulting from subprocess into pandas dataframe
import pandas as pd
import subprocess
import datetime
import os
from io import StringIO

def fetch_reddit_posts():
    try:
        output = subprocess.run("go run main.go", shell=True, cwd="tools/reddit", capture_output=True)
        raw_text = output.stdout.decode("utf-8")
        # read raw text in csv format in pandas df
        csvStringIO = StringIO(raw_text)
        print(raw_text)
        df = pd.read_csv(csvStringIO, sep="\t", on_bad_lines='warn')
        return df
    except Exception as e:
        print("FAILING TO PARSE ARTICLES")
        print(e)
        return None

def make_dirs(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)

def parse_reddit_posts(df: pd.DataFrame)-> None:
    # get curr month from curr date
    curr_month = datetime.datetime.now().strftime("%B")
    base_folder = f"data/reddit/{curr_month}"
    make_dirs(base_folder)
    # date in YYYY_MM_DD format plus - pre/post
    file_name = f"{datetime.datetime.now().strftime('%Y_%m_%d')}_pre.csv"
    # make folder for reddit data
    csv_path = f"{base_folder}/{file_name}"
    df.to_csv(csv_path, index=False)
    return df

def main():
    df = fetch_reddit_posts()
    if df is not None and len(df) > 0:
        parse_reddit_posts(df)

if __name__ == '__main__':
    main()
