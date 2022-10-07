import subprocess
import pandas as pd

def openbb_economy():
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