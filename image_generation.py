import imgkit


def generate():
    cfg = imgkit.config()
    path = 'templates/index.html'
    weather = open(path, 'r').read()
    imgkit.from_string(weather, path, config=cfg)
    html_file = open('static/weather.jpg', 'w')
    html_file.write(weather)
