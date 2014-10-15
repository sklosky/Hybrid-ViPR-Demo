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
            myInfo = models.run_capture(hashtag)
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
    form = OptionsForm(request.form, twitter1='This is a test')
    error = None
    myInfo = None
    if request.method == 'POST':
        myInfo = models.update_options(form)
    return render_template('user/options.html', form=form, error=error, myInfo=myInfo)

@app.route('/about' , methods=['GET'])
def about():
    error = None
    myInfo = None
    return render_template('user/about.html', error=error, myInfo=myInfo)