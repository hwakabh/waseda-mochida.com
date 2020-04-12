from flask import Flask
from flask import render_template
from flask import send_from_directory
from flask import request
from linepay import LinePayApi

from socket import gethostname
import os
import uuid

app = Flask(__name__)


# LINE Pay API config and instanciate
LINE_PAY_CHANNEL_ID = os.environ.get('LINE_PAY_CHANNEL_ID')
LINE_PAY_CHANNEL_SECRET = os.environ.get('LINE_PAY_CHANNEL_SECRET')
LINE_PAY_IS_SANDBOX = False
LINE_PAY_SANDBOX_URL = 'https://api-pay.line.me'
CACHE = {}

if 'hwakabh' in gethostname():
    SERVER_URL = 'http://localhost:5000'
else:
    SERVER_URL = 'https://waseda-mochida.herokuapp.com/'

api = LinePayApi(
    LINE_PAY_CHANNEL_ID,
    LINE_PAY_CHANNEL_SECRET,
    is_sandbox=LINE_PAY_IS_SANDBOX
)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static/img'),
        'favicon.ico',
    )


# Member-Only: LINE Pay Transactions
@app.route('/member')
def member():
    return render_template('member.html')


# Initial User contact-point
# With this method, seller would receive paymentURL from RequestAPI and would notice to user
@app.route('/member/pay/request')
def linepay_request():
    order_id = str(uuid.uuid4())
    amount = 1
    currency = 'JPY'
    print('\n>>> Requesting to LINE Pay API for transaction reservation.')
    print('>>> Order ID: {}'.format(order_id))
    # Set caches
    CACHE['order_id'] = order_id
    CACHE['amount'] = amount
    CACHE['currency'] = currency
    # Build request body
    req = {
      'amount': amount,
      'currency': currency,
      'orderId': order_id,
      'packages': [
        {
          'id': 'package-999',
          'amount': 1,
          'name': 'Sample package',
          'products': [
            {
              'id': 'product-001',
              'name': 'Sample product',
              'imageUrl': 'https://placehold.jp/99ccff/003366/150x150.png?text=Sample%20product',
              'quantity': 1,
              'price': 1
            }
          ]
        }
      ],
      'redirectUrls': {
        'confirmUrl': SERVER_URL + '/member/pay/confirm',
        'cancelUrl': SERVER_URL + '/member/pay/cancel'
      }
    }
    print('\n>>> Calling Request API ... req-body: ')
    print(req)
    res = api.request(req)
    print('\n>>> Response from API ... res-body: ')
    print(res)
    return render_template('request.html', result=res)


# Confirm API called after user confirmation
# With this function, seller would be confirmed by LINE Pay API
@app.route('/member/pay/confirm')
def linepay_confirm():
    print('\n>>>> Cached data: ')
    print(CACHE)
    transaction_id = int(request.args.get('transactionId'))
    CACHE['transaction_id'] = transaction_id
    print('\n>>> Calling Confirm API with transaction: {}'.format(transaction_id))
    res = api.confirm(
        transaction_id=transaction_id,
        # Python SDK of Confirm API would expects amount as float value
        amount=float(CACHE.get('amount', 0)),
        currency=CACHE.get('currency', 'JPY')
    )
    print('\n>>> Responce from API ...')
    print(res)
    print('\n>>> Checking payment status: ')
    check_result = api.check_payment_status(transaction_id=transaction_id)
    print(check_result)
    print('\n>>> Checking payment details: ')
    pay_detail = api.payment_details(transaction_id=transaction_id)
    print(pay_detail)
    print('\n>>> Building body to render complete-template:')
    res['transaction_id'] = transaction_id
    res['paymentStatusCheckReturnCode'] = check_result.get('returnCode', None)
    res['paymentStatusCheckReturnMessage'] = check_result.get('returnMessage', None)
    res['payment_details'] = pay_detail
    return render_template('complete.html', result=res)


if __name__ == '__main__':
    HOST = 'localhost'
    PORT = 5000
    # Running configs
    app.debug = True
    app.threaded = True
    app.run(host=HOST, port=PORT)
