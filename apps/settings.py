import os


class LinePayConfigs():
    ACCOUNT_URL = 'https://line.me/R/ti/p/%40500xaweq'

    CHANNEL_ID = os.environ.get('LINE_PAY_CHANNEL_ID')
    CHANNEL_SECRET = os.environ.get('LINE_PAY_CHANNEL_SECRET')
    IS_SANDBOX = False
    SANDBOX_URL = 'https://api-pay.line.me'


class MailConfigs():
    FROM_ADDRESS = 'mochida.waseda@gmail.com'
    TO_ADDRESS = 'sukekiyoooooi@gmail.com'
    BCC = os.environ.get('EMAIL_BCC_ADDRESS')

    MY_PASSWORD = os.environ.get('EMAIL_GOOGLE_PASSWORD')


class AppConfigs():
    PIPELINE = os.environ.get('PIPELINE')

    if PIPELINE == 'local':
        SERVER_URL = 'http://localhost:5000'
    elif PIPELINE == 'stage':
        SERVER_URL = 'https://dev-waseda-mochida.herokuapp.com'
    elif PIPELINE == 'production':
        SERVER_URL = 'https://www.waseda-mochida.com'
