"""The Flask app, with initialization and view functions."""

import logging
import flask

from flask import Flask
from flask import abort, jsonify, redirect, render_template, request, url_for , flash
from flask.ext.login import LoginManager, current_user
from flask.ext.login import login_user, login_required, logout_user
from flask.ext.sqlalchemy import SQLAlchemy

from sched import config, filters, models
from sched.forms import CaptureForm
from shelljob import proc

app = Flask(__name__)
app.config.from_object(config)

# Load custom Jinja filters from the `filters` module.
filters.init_app(app)

# Setup logging for production.
if not app.debug:
    app.logger.setHandler(logging.StreamHandler()) # Log to stderr.
    app.logger.setLevel(logging.INFO)

@app.route( '/stream' )
def stream():
    g = proc.Group()
    p = g.run( [ "ls", "-R", "/" ] )
    
    def read_process():
        while g.is_pending():
            lines = g.readlines()
            for proc, line in lines:
                yield line
    
    return flask.Response( read_process(), mimetype= 'text/plain' )

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
