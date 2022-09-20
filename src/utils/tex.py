import re

import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import table

def extract_tex_from_file(input_file: str, output_file: str):
    """
    Extracts tex content from a file and writes it to a file.
    """
        
    with open(input_file) as f:
        lines = f.readlines()

    type_start_line = None
    type_end_line = None
    matches = []

    for i in range(len(lines)):
        line = lines[i]
        # check for \begin{document} and \begin{document} ignore all %
        if re.search(r'\\begin{document}', line):
            type_start_line = i
        elif re.search(r'\\end{document}', line):
            type_end_line = i

    # put lines from type_start_line to type_end_line into matches
    for i in range(type_start_line+1, type_end_line):
        line = lines[i]
        matches.append(line)
    # check for braces in line

    # write output of types to file overmind/types/oaClientTypes.ts
    with open(output_file, 'w') as f:
        for match in matches:
            f.write("".join(match))

def plot_df_as_table(df: pd.DataFrame, filename: str = "table.png")-> None:
    """
        Save
    """
    fig, ax = plt.subplots(figsize=(16, 2))
    ax.xaxis.set_visible(False)  # hide the x axis
    ax.yaxis.set_visible(False)  # hide the y axis
    ax.set_frame_on(False)  # no visible frame, uncomment if size is ok
    tabla = table(ax, df, loc='upper right', colWidths=[0.16]*len(df.columns))  # where df is your data frame
    # tabla.auto_set_font_size(True) # Activate set fontsize manually
    tabla.auto_set_font_size(False) # Activate set fontsize manually
    tabla.set_fontsize(12) # if ++fontsize is necessary ++colWidths
    tabla.scale(1.2, 1.2) # change size table
    plt.savefig(filename, transparent=True)

if __name__ == "__main__":
    extract_tex_from_file("full.tex", "content.tex")