import requests

# TODO docker container 이름으로 변경
def notify():
    requests.post("http://localhost:8080/notify/event")