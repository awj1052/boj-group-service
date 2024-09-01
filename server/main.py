import service, datetime
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/point')
def score():
    now = datetime.datetime.now()
    print(f"[{now}] {request.method} /point {request.remote_addr}")
    year = now.year
    month = now.month
    json = service.get_score_by_month(year, month)
    res = service.get_score_by_event(year, month)
    for e in res:
        if not e in json:
            json[e] = 0
        json[e] += res[e]
    return json

if __name__ == "__main__":  
    app.run(host='0.0.0.0', port=8080)#, threaded = False)

    # gunicorn -w 4 -b 0.0.0.0:8080 main:app
    