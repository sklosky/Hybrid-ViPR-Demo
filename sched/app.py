"""The Flask app, with initialization and view functions."""

import logging
import flask

from flask import Flask
from flask import abort, jsonify, redirect, render_template, request, url_for, flash, session
from flask.ext.login import LoginManager, current_user
from flask.ext.login import login_user, login_required, logout_user
from flask.ext.sqlalchemy import SQLAlchemy

from sched import config, filters, models
from sched.forms import CaptureForm, OptionsForm
from shelljob import proc

app = Flask(__name__)
app.config.from_object(config)
app.config['SECRET_KEY'] = 'F34TF$($e34D';

# Load custom Jinja filters from the `filters` module.
filters.init_app(app)

# Setup logging for production.
if not app.debug:
    app.logger.setHandler(logging.StreamHandler()) # Log to stderr.
    app.logger.setLevel(logging.INFO)

@app.errorhandler(404)
def error_not_found(error):
    """Render a custom template when responding with 404 Not Found."""
    return render_template('error/not_found.html'), 404

@app.route('/capture/', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def capture():
    form = CaptureForm(request.form)
    error = None
    myInfo = None
    if request.method == 'POST' and form.validate():
        hashtag = form.hashtag.data.lower().strip()
        if len(hashtag) > 0:
            sessionData = get_session_data()
            myInfo = models.run_capture(hashtag, sessionData)
    return render_template('user/capture.html', form=form, error=error, myInfo=myInfo)

@app.route('/analyze' , methods=['GET','POST'])
def analyze():
    error = None
    myInfo = None
    if request.method == 'POST':
        myInfo = models.run_analyze()
    return render_template('user/analyze.html', error=error, myInfo=myInfo)

@app.route('/options' , methods=['GET','POST'])
def options():
    sessionData = get_session_data()
    form = OptionsForm(request.form, twitter1=sessionData['twitter1'], twitter2=sessionData['twitter2'], twitter3=sessionData['twitter3'], twitter4=sessionData['twitter4'], viprOnline=sessionData['viprOnline'], s3secret=sessionData['s3secret'], s3user=sessionData['s3user'], s3host=sessionData['s3host'], s3port=sessionData['s3port'], s3bucket=sessionData['s3bucket'], maxTweets=sessionData['maxTweets'])
    error = None
    myInfo = None
    if request.method == 'POST':
        myInfo = set_session_data(form)
    return render_template('user/options.html', form=form, error=error, myInfo=myInfo)

@app.route('/about' , methods=['GET'])
def about():
    error = None
    myInfo = None
    return render_template('user/about.html', error=error, myInfo=myInfo)

def get_session_data():
    sessionData = {}
    if 'initialized' not in session:
        #session variables have not been set
        #set default values
        session['twitter1'] = 'XwWIvskkKUm6T5gJ3dofNt7lT'
        session['twitter2'] = 'ScSrr6ALpJJVNW9CnegmwFpKceZ3OBLULUeKfcWkpHumsffF2W'
        session['twitter3'] = '901773816-mA5lkLrPlUp5LRj5GisZVz28mJgeXctwSce4cm6u'
        session['twitter4'] = 'BEwO4nxfpTMmH4Pj575nJDPZPiaB2tavngYWyE4k3HUqz'
        session['viprOnline'] = 'True'
        session['s3secret'] = 'pBdWy02VWtuB3KuOWvFfJp8tiOCVIQDLvAkrou/p'
        session['s3user'] = 'root'
        session['s3host'] = '192.168.1.80'
        session['s3port'] = 9020
        session['s3bucket'] = 'myNewBucket'
        session['maxTweets'] = 100
        session['initialized'] = 'True'
    #get values from session variables
    sessionData['twitter1'] = session['twitter1']
    sessionData['twitter2'] = session['twitter2']
    sessionData['twitter3'] = session['twitter3']
    sessionData['twitter4'] = session['twitter4']
    sessionData['viprOnline'] = session['viprOnline']
    sessionData['s3secret'] = session['s3secret']
    sessionData['s3user'] = session['s3user']
    sessionData['s3host'] = session['s3host']
    sessionData['s3port'] = session['s3port']
    sessionData['s3bucket'] = session['s3bucket']
    sessionData['maxTweets'] = session['maxTweets']
    return sessionData

def set_session_data(form):
    session['twitter1'] = form.twitter1.data
    session['twitter2'] = form.twitter2.data
    session['twitter3'] = form.twitter3.data
    session['twitter4'] = form.twitter4.data
    session['viprOnline'] = form.viprOnline.data
    session['s3secret'] = form.s3secret.data
    session['s3user'] = form.s3user.data
    session['s3host'] = form.s3host.data
    session['s3port'] = form.s3port.data
    session['s3bucket'] = form.s3bucket.data
    session['maxTweets'] = form.maxTweets.data
    return