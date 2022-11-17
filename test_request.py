import requests

url = "http://localhost:8000/ping"
r = requests.get(url)
print()
print(r.text + "\n")
