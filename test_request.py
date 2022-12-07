import requests
import time

url = "http://localhost:8000/hostname"
for i in range(5):
    r = requests.get(url)
    print()
    print(r.text + "\n")
    time.sleep(2)

