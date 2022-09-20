import os 
import requests


def send_file(path: str) -> None:
    """ send discord file from path to discord using requests"""
    url = os.getenv("DISCORD_WEBHOOK")
    files = {'file': open(path, 'rb')}
    data = {
        "username": "MarketWatch",
        "content": "MarketWatch Report",
    }
    requests.post(url, files=files, data=data)

    

if __name__ == '__main__':
    send_file("data/latest.pdf")