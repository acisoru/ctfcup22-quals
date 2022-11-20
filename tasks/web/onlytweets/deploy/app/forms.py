import re

from wtforms import StringField, URLField
from flask_wtf import FlaskForm, RecaptchaField
from wtforms.validators import input_required, Regexp


class IsURL(Regexp):
    def __init__(self, message=None):
        regex = (
            r"^(http|https)://"
            r"(?P<host>[^\/\?:]+)"
            r"(?P<port>:[0-9]+)?"
            r"(?P<path>\/.*?)?"
            r"(?P<query>\?.*)?$"
        )
        super(IsURL, self).__init__(regex, re.IGNORECASE, message)

    def __call__(self, form, field, msg=None):
        message = self.message
        if message is None:
            message = field.gettext('Invalid URL.')

        super(IsURL, self).__call__(form, field, message)


class ReportForm(FlaskForm):
    report_url = URLField('Report URL:', [input_required(), IsURL()])
    recaptcha = RecaptchaField()

