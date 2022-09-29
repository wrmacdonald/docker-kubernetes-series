import requests

url = "http://localhost:8000/predict"
data = {"prediction_window": 7}
r = requests.post(url, json=data)
