# parse reddit data resulting from subprocess into pandas dataframe
import pandas as pd
import subprocess
import datetime
import os
from io import StringIO

def fetch_reddit_posts():
    try:
        output = subprocess.run("go run main.go", shell=True, cwd="../tools/reddit", capture_output=True)
        raw_text = output.stdout.decode("utf-8")
        # read raw text in csv format in pandas df
        csvStringIO = StringIO(raw_text)
        df = pd.read_csv(csvStringIO, sep=",")
        # df = pd.read(raw_text)
        print(df)
        return df
    except Exception as e:
        print(e)
        return None

def make_dirs(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)

def parse_reddit_posts(df: pd.DataFrame)-> None:
    print(df)
    # get curr month from curr date
    curr_month = datetime.datetime.now().strftime("%B")
    print(curr_month)
    base_folder = f"../data/reddit/{curr_month}"
    make_dirs(base_folder)
    # date in YYYY_MM_DD format plus - pre/post
    file_name = f"{datetime.datetime.now().strftime('%Y_%m_%d')}-post.csv"
    # make folder for reddit data
    csv_path = f"{base_folder}/{file_name}"
    df.to_csv(csv_path, index=False)
    return df
    pass

def main():
    df = fetch_reddit_posts()
    if df is not None:
        parse_reddit_posts(df)

if __name__ == '__main__':
    main()