# flask app that serves the index.html file

from flask import Flask, render_template

name = 'zumbi'
app = Flask(name)


@app.route("/")
def index():
    return render_template('./index.html')


@app.route("/admin")
def admin():
    return render_template('./admin.html')


def start_webapp():
    app.run(host='0.0.0.0', port=4002, ssl_context='adhoc')


if __name__ == '__main__':
    start_webapp()