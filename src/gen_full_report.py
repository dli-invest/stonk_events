# write_messages.py
import re
import glob
from datetime import datetime
from jinja2 import Environment, FileSystemLoader


environment = Environment(loader=FileSystemLoader(""))
template = environment.get_template("data/lwarp_template.jinja2")

pattern = r'\\begin\{document\}(.*?)\\end\{document\}'

reports = []
# iterate through all tex files in data/reports/**/*.tex  using glob
last_month = None
for report_path in glob.glob("data/reports/**/*.tex"):
    # read tex file
    with open(report_path, "r", encoding="utf-8") as f:
        tex = f.read()
    # parse tex file
    # parse table captions
    report_content = re.findall(pattern, tex, re.DOTALL)
    # check if contains pre or post
    # extract date from report_2022_09_22_pre.tex, grab 2022-09-22
    report_filename = report_path.split("/")[-1]
    report_date = "-".join(report_filename.split("_")[1:4])
    report_type = report_filename.split("_")[4].split(".")[0]
    # add chapter if a new month is found, use datetime, format (%B)
    curr_month = datetime.strptime(report_date, "%Y-%m-%d").strftime("%B %Y")
    report_data = {
        "report_type": report_type,
        "report_date": report_date,
        "lines": report_content[0].split("\n"),
        "chapter": False,   
    }
    if curr_month != last_month:
        report_data["chapter"] = curr_month
        last_month = curr_month
    # move images files in img folder to data/reports/img, this is for monthly reports
    reports.append(report_data)

context = {
    "reports": reports
}

# todo may need report for pre and post, probably just combine both
full_report_path = "data/full_report.tex"

with open(full_report_path, mode="w", encoding="utf-8") as results:
    results.write(template.render(context))
    print(f"... wrote {full_report_path}")
