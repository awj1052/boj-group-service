import service, datetime, pytz
from flask import Flask, render_template, url_for, request
from flask_cors import CORS

import logger
from logger import msg, warning, error, debug, LogLevel

logger.set_level(LogLevel.DEBUG)
app = Flask(__name__)
CORS(app)

timezone = pytz.timezone('Asia/Seoul')

scores = service.get_score()
ranks = service.get_score_and_rank(scores)
lotto = service.get_shuffle(ranks)
logs = service.get_log()
events = service.get_events()

@app.route('/')
def default():
    # msg(f"{request.method} / {request.remote_addr}")
    now = datetime.datetime.now(timezone).replace(tzinfo=None)
    return render_template('anabada.html', ranks=ranks, lotto=lotto, logs=logs, events=events, now=now)

@app.route('/notify/score', methods=['POST'])
def notify_score():
    global scores, ranks, lotto, logs
    msg("/notify/score called")
    scores = service.get_score()
    ranks = service.get_score_and_rank(scores)
    lotto = service.get_shuffle(ranks)
    logs = service.get_log()
    return 'OK', 200

@app.route('/notify/event', methods=['POST'])
def notify_event():
    global events
    msg("/notify/event called")
    events = service.get_events()
    return 'OK', 200

if __name__ == "__main__":  
    app.run(host='0.0.0.0', port=8080)#, threaded = False)

    # gunicorn -w 1 --threads=4 -b 0.0.0.0:8080 main:app
    