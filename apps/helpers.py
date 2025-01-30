from datetime import datetime, timedelta
from io import BytesIO
import base64

import qrcode
from PIL import Image


# Functions to calculate next online event day
def get_next_thursday(t):
    day_1 = datetime(2020, 6, 11)
    offset = 14 - ((t - day_1).days % 14)
    return t + timedelta(days=offset)


def generate_qr_code_data(url):
    q = qrcode.make(url)

    # Write Buffer for storing QR code data
    bf = BytesIO()
    q.save(bf, format='png')

    # Return binary data of QR Codes
    return base64.b64encode(bf.getvalue()).decode("utf-8")

