import re

with open('./full.tex') as f:
    lines = f.readlines()


# scan for export interface and export type
type_start = 0
found_export = False

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
with open('template_doc.py', 'w') as f:
    for match in matches:
        f.write("".join(match))
