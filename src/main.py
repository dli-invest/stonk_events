# all tex related stuff is in src/tex.py
import numpy as np
import pylatex as pl
import pandas as pd
import shutil
import os
import requests
from discord import Webhook, RequestsWebhookAdapter
from datetime import datetime
from marketwatch import split_table, get_tables
from utils import plot_df_as_table
from tex import make_report

# expect this file to be run in root directory where README.md is
def main():
    # read config file, either json or ini file to get report type
    tables = get_tables()

    report_data = dict(tables =tables)

    # get date in YYYY_MM_DD format from current date
    curr_date = datetime.now().strftime("%Y_%m_%d")
    report_name = f"reports/{curr_date}.tex"
    make_report(report_data, report_name)
    # copy report_name file to reports/latest.tex
    shutil.copy(report_name, "reports/latest.tex")

    plot_df_as_table(tables[0])
    # get DISCORD_WEBHOOK from env vars
    DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")
    # https://discord.com/api/webhooks/960318997243506699/vlhaXdT---0UUH1FSU0QvP8GMmxIK1H2pTwkieI1Jg7blH7jEB7jbnynqQcf2NdDmNg6
    webhook = Webhook.from_url(DISCORD_WEBHOOK, adapter=RequestsWebhookAdapter())
    webhook.send('Sending Files', username='earning_events', file="reports/latest.tex")
    webhook.send('Sending Files', username='earning_events', file="table.png")
    webhook.send('Sending Files', username='earning_events', file="reports/latest.pdf")
    # use discord to send image to channel



    # make table image to send to discord

    # send table 0 to discord

# test_table = dfs[2]
# # trip Report column to 15 characters
# test_table["Report"] = test_table["Report"].str.slice(0, 25)
# plot_df_as_table(test_table)
if __name__ == "__main__":
    main()
