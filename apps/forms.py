from flask_wtf import Form, RecaptchaField
from wtforms import TextAreaField, StringField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length, Email


class ContactForm(Form):
      name      = StringField('お名前', validators=[DataRequired(), Length(max=255)])
      email     = StringField('メールアドレス', validators=[InputRequired(), Email()])
      message   = TextAreaField('ご予約・お問い合わせ内容', validators=[DataRequired()])
      recaptcha = RecaptchaField()
      submit    = SubmitField('送信')
