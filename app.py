import datetime
import json
from datetime import datetime

import requests
from flask import Flask
from flask import render_template

app = Flask(__name__)
config = json.load(open('json/config.json', 'r'))
last_call_time = datetime.fromisoformat('2008-10-10').timestamp()
http_response = None


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
    return render_template('index.html', days=config['days'], data=data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config['port'])
