import service, datetime, os, sys
from flask import Flask, render_template, url_for, request
from flask_cors import CORS
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import logger
from logger import msg, warning, error, debug, LogLevel

logger.set_level(LogLevel.DEBUG)
app = Flask(__name__)
CORS(app)

@app.route('/')
def default():
    msg(f"{request.method} / {request.remote_addr}")
    scores = service.get_score()
    ranks = service.get_score_and_rank(scores)
    lotto = service.get_shuffle(scores)
    logs = service.get_log()
    events = service.get_events()
    return render_template('anabada.html', ranks=ranks, lotto=lotto, logs=logs, events=events, now=datetime.datetime.now())

if __name__ == "__main__":  
    app.run(host='0.0.0.0', port=8080)#, threaded = False)

    # gunicorn -w 4 -b 0.0.0.0:8080 main:app
    