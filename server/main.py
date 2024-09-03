import service, datetime
from flask import Flask, render_template, url_for, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def default():
    service.get_score()
    return render_template('anabada.html', test="asd")

@app.route('/point')
def score():
    return service.get_score()

if __name__ == "__main__":  
    app.run(host='0.0.0.0', port=8080)#, threaded = False)

    # gunicorn -w 4 -b 0.0.0.0:8080 main:app
    