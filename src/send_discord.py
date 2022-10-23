import os 
import requests
import argparse


def send_file(path: str, content = "MarketWatch Report", username="Marketwatch") -> None:
    """ send discord file from path to discord using requests"""
    url = os.getenv("DISCORD_WEBHOOK")
    files = {'file': open(path, 'rb')}
    data = {
        "username": username,
        "content": content,
    }
    requests.post(url, files=files, data=data)

    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, required=False, default="latest.pdf")
    parser.add_argument("--content", type=str, required=False, default="MarketWatch Report")
    parser.add_argument("--username", type=str, required=False, default="Marketwatch")
    args = parser.parse_args()
    send_file(args.path, args.content, args.username)