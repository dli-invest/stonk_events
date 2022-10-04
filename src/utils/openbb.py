import subprocess
import pandas as pd
p = subprocess.Popen(["python", "terminal.py", "exe", "../tools/openbb/economy_overview.openbb"], cwd="OpenBBTerminal", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate()
print(out)

# get all lines with Saved file: up until newline
for line in out.splitlines():
    if b"Saved file:" in line:
        # print(line)
        # get the file path
        file_path = line.split(b"Saved file:")[1].strip().decode()
        print(file_path)
        df = pd.read_csv(file_path, index_col=0)
        print(df)
        # read file and print
# get result from openbb terminal