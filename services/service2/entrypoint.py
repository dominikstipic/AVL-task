import requests
import sys

def process(url):
    SERVICE1_URL = "http://service1:8080"
    message = requests.get(url).text
    data = ["md5", message]
    body = "\n".join(data)
    body = body.encode("utf-8")
    result = requests.post(SERVICE1_URL, data=body)
    return result.text

if __name__ == "__main__":
    arg = sys.stdin.readline()
    print(f"url={arg}")
    h = process(arg)
    print(f"{h}")