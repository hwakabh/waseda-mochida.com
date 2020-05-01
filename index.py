from flask import Flask
from flask import render_template
from flask import send_from_directory
from flask import request
from linepay import LinePayApi

from socket import gethostname
import os
import uuid
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
import ssl
import sys


app = Flask(__name__)

# Email parameters
FROM_ADDRESS = 'mochida.waseda@gmail.com'
MY_PASSWORD = os.environ.get('EMAIL_GOOGLE_PASSWORD')
TO_ADDRESS = 'sukekiyoooooi@gmail.com'
BCC = os.environ.get('EMAIL_BCC_ADDRESS')
SUBJECT = ''
BODY = ''
REQUEST_EMAIL_ADDR = ''

# LINE Pay API config and instanciate
LINE_PAY_CHANNEL_ID = os.environ.get('LINE_PAY_CHANNEL_ID')
LINE_PAY_CHANNEL_SECRET = os.environ.get('LINE_PAY_CHANNEL_SECRET')
LINE_PAY_IS_SANDBOX = False
LINE_PAY_SANDBOX_URL = 'https://api-pay.line.me'

if (LINE_PAY_CHANNEL_ID is None) or (LINE_PAY_CHANNEL_SECRET is None):
    print('>>> Precheck failed.')
    print('Environmental variables for LINE API missing, set LINE_PAY_CHANNEL_ID and LINE_PAY_CHANNEL_SECRET first.\n')
    sys.exit(1)

CACHE = {}
global amount

if 'hwakabh' in gethostname():
    SERVER_URL = 'http://localhost:5000'
else:
    SERVER_URL = 'https://www.waseda-mochida.com'

api = LinePayApi(
    LINE_PAY_CHANNEL_ID,
    LINE_PAY_CHANNEL_SECRET,
    is_sandbox=LINE_PAY_IS_SANDBOX
)


@app.route('/')
def index():
    return render_template('index.html', data={
        'is_member_only': False,
        'page_from': request.method,
    })


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static/img'),
        'favicon.ico',
    )


@app.route('/mail', methods=['POST'])
def mail():
    def build_mailbody(from_addr, to_addr, subject, body):
        mail = MIMEText(body)
        mail['From'] = from_addr
        mail['To'] = to_addr
        mail['Subject'] = subject
        mail['Date'] = formatdate()
        if BCC is not None:
            mail['Bcc'] = BCC
        else:
            mail['Bcc'] = ''
        return mail

    REQUEST_USERNAME = request.form['name']
    REQUEST_EMAIL_ADDR = request.form['email']
    # Add REQUEST_EMAIL_ADDR in BODY as content
    BODY = 'Contact from {0}\n email: {1}\n\n{2}\n{3}\n{4}\n'.format(
        REQUEST_USERNAME,
        REQUEST_EMAIL_ADDR,
        '-' * 10,
        request.form['message'],
        '-' * 10
    )
    print('>>> Email sending requested.')
    print('name: {}'.format(REQUEST_USERNAME))
    print('email: {}'.format(REQUEST_EMAIL_ADDR))
    print('message: \n\n{}'.format(BODY))

    draft = build_mailbody(from_addr=FROM_ADDRESS, to_addr=TO_ADDRESS, subject=SUBJECT, body=BODY)

    # try to send email
    print('>>> Sending to email to administrator : {}...'.format(TO_ADDRESS))
    print(draft)
    #context = ssl.create_default_context()
    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10)
    smtp.login(FROM_ADDRESS, MY_PASSWORD)
    smtp.sendmail(FROM_ADDRESS, TO_ADDRESS, draft.as_string())
    smtp.close()

    # If success
    return render_template('mail.html', data={
        'is_member_only': False,
        'request_name': REQUEST_USERNAME,
        'request_email': REQUEST_EMAIL_ADDR,
        'request_body': request.form['message'].splitlines(),
    })
    # If failed like SMTPAuthenticationError, return to sorry-page and guide user to send email admin directly


# Member-Only: LINE Pay Transactions
@app.route('/member')
def member():
    return render_template('member.html', data={
        'is_member_only': True
    })


# Initial User contact-point
# With this method, seller would receive paymentURL from RequestAPI and would notice to user
@app.route('/member/pay/request', methods=['GET', 'POST'])
def linepay_request():
    if request.method == 'POST':
        amount = int(request.form['amount'])
    else:
        amount = 0
        print('>>> Error with user selection, none of the amount selected.')
    
    if (amount == 1000) or (amount == 3000):
        menu = '{} 円セット'.format(amount)
    elif amount == 5000:
        menu = 'ちょい漢気 5000 円セット'
    elif amount == 10000:
        menu = '漢気 10000 円セット'
    else:
        menu = '未選択'

    order_id = str(uuid.uuid4())
    currency = 'JPY'
    print('\n>>> Requesting to LINE Pay API for transaction reservation.')
    print('Order ID: {}'.format(order_id))
    print('Ordered menu: {}'.format(menu))
    print('Purchase amount: {0} {1}'.format(currency, amount))
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
          'amount': amount,
          'name': '来店メニュー',
          'products': [
            {
              'id': 'product-001',
              'name': menu,
              'imageUrl': '{0}/static/img/return_{1}.jpg'.format(SERVER_URL, amount),
              'quantity': 1,
              'price': amount
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
    res['menu'] = menu
    res['amount'] = amount
    return render_template('request.html', data={
        'result': res,
        'is_member_only': True
    })


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
        amount=float(CACHE.get('amount', amount)),
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
    return render_template('complete.html', data={
        'result': res,
        'is_member_only': True
    })


# Refund API called if user ordered wrong one
@app.route('/member/pay/refund', methods=['POST'])
def linepay_refund():
    if request.method == 'POST':
        transaction_id = int(request.form['transaction_id'])
        CACHE = {}
    else:
        transaction_id = 0
        print('>>> Error with user selection, could not fetch transaction_id')
    print('\n>>> Calling Refund API with transaction: {0}'.format(transaction_id))
    print('Starting refund operation for transaction_id: {0}'.format(transaction_id))
    res = api.refund(transaction_id)
    print(res)
    res['source_transaction_id'] = transaction_id
    return render_template('refund.html', data={
        'result': res,
        'is_member_only': True
    })


# Refund API called if user ordered wrong one
@app.route('/member/pay/cancel', methods=['GET'])
def linepay_cancel():
    res = request.args
    print('\n>>> Calling cancelUrl with transaction.')
    if res:
        print(res)
        transaction_id = res.get('transactionId')
        CACHE = {}
    else:
        print('Failed to get response-body from cancelUrl.')
    print('\n>>> Cancellation for transaction : {0} complete.'.format(transaction_id))
    return render_template('cancel.html', data={
        'result': res,
        'is_member_only': True
    })


if __name__ == '__main__':
    HOST = 'localhost'
    PORT = 5000
    # Running configs
    app.debug = True
    app.threaded = True
    app.run(host=HOST, port=PORT)
