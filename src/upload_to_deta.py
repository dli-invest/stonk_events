import argparse
import os
import subprocess
from deta import Deta



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="File to upload to Deta Base")
    parser.add_argument("report_name", help="Name of the report")
    args = parser.parse_args()

    # read DETA_TOKEN from environment variable
    deta = Deta(os.environ["DETA_TOKEN"])

    drive = deta.Drive("stonk_events")
    with open(args.file, "r") as f:
        drive.put(args.report_name, f)
        f.close()