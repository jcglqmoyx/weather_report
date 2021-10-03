import datetime
import logging
from datetime import datetime

import requests
from flask import Flask, request
from flask import render_template
from gevent import pywsgi

import json

app = Flask(__name__)
config = json.load(open('json/config.json', 'r'))
last_call_time = datetime.fromisoformat('2008-10-10').timestamp()
http_response = None
cnt = 0

@app.route('/')
def weather():
    global last_call_time, http_response
    city_code = config['city_code']
    url = config['api'] + city_code
    now = datetime.now().timestamp()
    diff = now - last_call_time
    if diff > config['update-interval']:
        http_response = requests.get(url)
        last_call_time = now
    data = json.loads(http_response.text)
    ip = request.remote_addr
    global cnt
    cnt += 1
    logging.basicConfig(filename='log.txt', level=logging.INFO)
    logging.info('第' + str(cnt) + '次调用, IP: ' + ip)
    return render_template('index.html', days=config['days'], data=data)


if __name__ == '__main__':
    server = pywsgi.WSGIServer(('0.0.0.0', config['port']), app)
    server.serve_forever()
