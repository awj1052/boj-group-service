import requests

def notify():
    requests.post("http://localhost:8080/notify/event")