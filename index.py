from flask import Flask
from flask import render_template
from flask import send_from_directory
from linepay import LinePayApi

import os


app = Flask(__name__)


# LINE Pay API config and instanciate
LINE_PAY_CHANNEL_ID = os.environ.get("LINE_PAY_CHANNEL_ID")
LINE_PAY_CHANNEL_SECRET = os.environ.get("LINE_PAY_CHANNEL_SECRET")
LINE_PAY_IS_SANDBOX = False
api = LinePayApi(
    LINE_PAY_CHANNEL_ID,
    LINE_PAY_CHANNEL_SECRET,
    is_sandbox=LINE_PAY_IS_SANDBOX
)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/member')
def member():
    return render_template('member.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static/img'),
        'favicon.ico',
    )


if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 5000
    # Running configs
    app.debug = True
    app.threaded = True
    app.run(host=HOST, port=PORT)
