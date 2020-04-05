from flask import Flask
from flask import render_template
from flask import request


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 5000
    # Running configs
    app.debug = True
    app.threaded = True
    app.run(host=HOST, port=PORT)
