import subprocess
import pandas as pd
from openbb_terminal.sdk import openbb
from openbb_terminal.economy.wsj_model import market_overview, us_indices, us_bonds, top_commodities, global_bonds, global_currencies

def weekly_lows():
    # 52 week low
    new_low_df = openbb.stocks.screener.screener_data(preset_loaded='new_low', data_type = 'overview')
    return new_low_df 


def openbb_economy():
    """Open the Blackboard website in the default web browser."""
    economy_dfs = []
    file_names = []
    # append two entries to economy dfs from top_commodities and us_bonds
    economy_dfs.append(top_commodities())
    file_names.append("top_commodities")
    economy_dfs.append(us_bonds())
    file_names.append("us_bonds")
    economy_dfs.append(us_indices())
    file_names.append("us_indices")
    economy_dfs.append(global_bonds())
    file_names.append("global_bonds")
    economy_dfs.append(global_currencies())
    file_names.append("global_currencies")
    economy_dfs.append(market_overview())
    file_names.append("market_overview")

    return economy_dfs, file_names

def openbb_economy_legacy():
    """Open the Blackboard website in the default web browser."""
    p = subprocess.Popen(["python", "terminal.py", "exe", "../tools/openbb/economy_overview.openbb"], cwd="OpenBBTerminal", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    economy_dfs = []
    file_names = []
    # get all lines with Saved file: up until newline
    for line in out.splitlines():
        if b"Saved file:" in line:
            # print(line)
            # get the file path
            file_path = line.split(b"Saved file:")[1].strip().decode()
            df = pd.read_csv(file_path, index_col=0)
            df.style.set_caption(file_path)
            economy_dfs.append(df)
            report_type = file_path.split("/")[-1].split("_")[-1]
            file_names.append(report_type)
    return economy_dfs, file_names
        # read file and print
# get result from openbb terminal

if __name__ == "__main__":
    economy_dfs, file_names = openbb_economy()