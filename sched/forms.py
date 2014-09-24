"""Forms to render HTML input & validate request data."""

from wtforms import Form, BooleanField, DateTimeField, PasswordField
from wtforms import TextAreaField, TextField
from wtforms.validators import Length, required

class CaptureForm(Form):
    """Render HTML input for hashtag form.

    Processing happens in the view function.
    """
    hashtag = TextField('Hashtag', [required()])
    """password = PasswordField('Password', [required()])"""
