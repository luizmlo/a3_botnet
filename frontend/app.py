# flask app that serves the index.html file

from flask import Flask, render_template

name = 'zumbi'

app = Flask(name)

@app.route("/")
def index():
    return render_template('./index.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4002, debug=True, ssl_context='adhoc')