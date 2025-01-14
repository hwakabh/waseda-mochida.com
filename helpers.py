from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.utils import formatdate


# Functions to calculate next online event day
def get_next_thursday(t):
    day_1 = datetime(2020, 6, 11)
    offset = 14 - ((t - day_1).days % 14)
    return t + timedelta(days=offset)


def build_mailbody(from_addr, to_addr, subject, body, bcc):
    mail = MIMEText(body)
    mail['From'] = from_addr
    mail['To'] = to_addr
    mail['Subject'] = subject
    mail['Date'] = formatdate()
    if bcc is not None:
        mail['Bcc'] = bcc
    else:
        mail['Bcc'] = ''
    return mail
