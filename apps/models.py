from datetime import datetime


from apps.database import db


class OrderHistory(db.Model):
    __tablename__: str = "order_history"

    # type is `purchase` or `refund`
    order_type  = db.Column(db.String(8))
    # aligned UUID v4
    order_id    = db.Column(db.String(36), primary_key=True)
    # https://help2.line.me/linepay_jp/android/pc?country=JP&lang=ja&contentId=20021203
    # expecting max JPY 100,000
    amount      = db.Column(db.Integer())
    menu        = db.Column(db.String(256), index=True)

    created_at  = db.Column(db.DateTime, nullable=False, default=datetime.now)
