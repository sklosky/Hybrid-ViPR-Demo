"""Forms to render HTML input & validate request data."""

from wtforms import Form, BooleanField, DateTimeField, PasswordField
from wtforms import TextAreaField, TextField
from wtforms.validators import Length, required
import models

class CaptureForm(Form):
    """Render HTML input for hashtag capture form.

    Processing happens in the view function.
    """
    hashtag = TextField('Hashtag', [required()])

class OptionsForm(Form):
    #Render HTML input for options form.
    #Processing happens in the view function.

    twitter1 = TextField('OAUTH Token')
    twitter2 = TextField('OAUTH Secret')
    twitter3 = TextField('Customer Key')
    twitter4 = TextField('Customer Secret')
    viprOnline = TextField('ViPR Online')
    s3secret = TextField('S3 Secret')
    s3user = TextField('S3 Username')
    s3host = TextField('S3 Hostname')
    s3port = TextField('S3 Port')
    s3bucket = TextField('S3 Bucket Name')
    maxTweets = TextField('Max Tweets to Capture')