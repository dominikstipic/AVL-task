import requests
import sys

SERVICE1_URL = "http://service1:8080"

arg = sys.stdin.readline()
print(f"input={arg}")

message = requests.get(arg).text
data = ["md5", message]

body = "\n".join(data)
body = body.encode("utf-8")
result = requests.post(SERVICE1_URL, data=body)
print(result.text)