from datetime import datetime
import os
import uuid
import sys

from flask import render_template
from flask import send_from_directory
from flask import request
from flask import jsonify
from flask_mail import Mail, Message
from flask_caching import Cache
from linepay import LinePayApi

from apps import create_app
from apps.helpers import get_next_thursday, generate_qr_code_data
from apps.settings import AppConfigs as config
from apps.settings import LinePayConfigs as line

app = create_app()
app.config.from_object('apps.settings.MailConfigs')
mail = Mail(app)

app.config.from_object('apps.settings.RedisConfigs')
cache = Cache(app)

# global amount

if config.PIPELINE is None:
    print('>>> Precheck failed.')
    print('Environmental variables PIPELINE missing, failed to start app.\n')
    sys.exit(1)


# LINE Pay API config and instanciate
if (line.CHANNEL_ID is None) or (line.CHANNEL_SECRET is None):
    print('>>> Precheck failed.')
    print('Environmental variables for LINE API missing, set LINE_PAY_CHANNEL_ID and LINE_PAY_CHANNEL_SECRET first.\n')
    sys.exit(1)

api = LinePayApi(
    line.CHANNEL_ID,
    line.CHANNEL_SECRET,
    is_sandbox=line.IS_SANDBOX
)


@app.route('/')
def index():
    # get base64-encoded string and render raw data to <img src="">
    qr = generate_qr_code_data(url=line.ACCOUNT_URL)

    return render_template('index.html', data={
        'is_member_only': False,
        'page_from': request.method,
        'line_qr_code': "data:image/png;base64,{}".format(qr)
    })


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static/img'),
        'favicon.ico',
    )


@app.route('/healthz')
def healthz():
    return jsonify({'status': 'ok'})


@app.route('/mail', methods=['POST'])
def send_mail():
    msg = Message()
    # person you can see in the field `from:` in the message
    # With Brevo, `from` fields looks like `SMTP_UESRNAME_BEFORE_ATMARK@BREVO_ID.brevosend.com`
    msg.sender = 'hrykwkbys1024@gmail.com'
    # Person who will get message (to:)
    msg.recipients = [
        'hwakabh@icloud.com',
        'hiro.wakabayashi@hashicorp.com'
    ]
    msg.subject = '[waseda-mochida] Contact from {}'.format(request.form.get('email'))
    msg.body = request.form.get('message')

    print('>>> Email sending requested.')
    print('- name: {}'.format(request.form.get('name')))
    print('- email: {}'.format(request.form.get('email')))
    print('- message: \n{}'.format(request.form.get('message')))

    is_success = True
    try:
        print(f'>>> Sending to email to administrator : {msg.sender}...')
        mail.send(msg)
    except Exception as e:
        is_success = False
        print('>>> Failed to send email ...')
        print(e)

    print('>>> Successfully send email.')

    return render_template('mail.html', data={
        'is_member_only': False,
        'request_name': request.form.get('name'),
        'request_email': request.form.get('email'),
        'request_body': request.form['message'].splitlines(),
        'is_success': is_success,
    })


# Member-Only: LINE Pay Transactions
@app.route('/member')
def member():
    today = datetime.now()
    next_event_day = get_next_thursday(t=today)

    return render_template('member.html', data={
        'is_member_only': True,
        'next_month': next_event_day.month,
        'next_day': next_event_day.day,
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
    cache.set('order_id', order_id)
    cache.set('amount', amount)
    cache.set('currency', currency)
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
              'imageUrl': '{0}/static/img/return_{1}.jpg'.format(config.SERVER_URL, amount),
              'quantity': 1,
              'price': amount
            }
          ]
        }
      ],
      'redirectUrls': {
        'confirmUrl': config.SERVER_URL + '/member/pay/confirm',
        'cancelUrl': config.SERVER_URL + '/member/pay/cancel'
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
    print(cache.get('amount'))
    print(cache.get('currency'))
    print(cache.get('order_id'))

    transaction_id = int(request.args.get('transactionId'))
    cache.set('transaction_id', transaction_id)
    print('\n>>> Calling Confirm API with transaction: {}'.format(transaction_id))
    # Python SDK of Confirm API would expects amount as float value
    res = api.confirm(
        transaction_id,
        float(cache.get('amount')),
        cache.get('currency')
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
        cache.clear()
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
        cache.clear()
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
