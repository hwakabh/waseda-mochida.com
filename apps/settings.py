import os


class LinePayConfigs(object):
    ACCOUNT_URL = 'https://line.me/R/ti/p/%40500xaweq'

    CHANNEL_ID = os.environ.get('LINE_PAY_CHANNEL_ID')
    CHANNEL_SECRET = os.environ.get('LINE_PAY_CHANNEL_SECRET')
    IS_SANDBOX = True
    SANDBOX_URL = 'https://api-pay.line.me'


class MailConfigs(object):
    # https://flask-mail.readthedocs.io/en/latest/#configuring
    MAIL_SERVER           = 'smtp-relay.brevo.com'
    MAIL_PORT             = 587
    MAIL_USE_TLS          = True
    MAIL_USE_SSL          = False
    MAIL_USERNAME         = 'hrykwkbys1024@gmail.com'
    MAIL_PASSWORD         = os.environ.get('BREVO_SMTP_KEY')
    # # default person you can see in the field `from:` in the message
    # MAIL_DEFAULT_SENDER   = 'hrykwkbys1024@gmail.com'


class RedisConfigs(object):
    # https://flask-caching.readthedocs.io/en/latest/#configuring-flask-caching
    CACHE_TYPE            = 'RedisCache'
    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_REDIS_URL       = os.environ.get('REDIS_URL')
    # CACHE_REDIS_HOST      = os.environ.get('REDIS_URL').split(':')[-2].split('@')[1]
    # CACHE_REDIS_PORT      = os.environ.get('REDIS_URL').split(':')[-1]
    # CACHE_REDIS_PASSWORD  = os.environ.get('REDIS_URL').split(':')[-1].split('@')[1]

class AppConfigs(object):
    PIPELINE = os.environ.get('PIPELINE')

    if PIPELINE == 'local':
        SERVER_URL = 'http://localhost:5000'
    elif PIPELINE == 'stage':
        SERVER_URL = 'https://dev-waseda-mochida.herokuapp.com'
    elif PIPELINE == 'production':
        SERVER_URL = 'https://www.waseda-mochida.com'
