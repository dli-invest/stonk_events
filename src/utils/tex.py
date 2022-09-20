import re

import pandas as pd
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


if __name__ == "__main__":
    extract_tex_from_file("full.tex", "content.tex")