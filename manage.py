from flask.ext.script import Manager

from sched.app import app


# By default, Flask-Script adds the 'runserver' and 'shell' commands to
# interact with the Flask application. Add additional commands using the
# `@manager.command` decorator, where Flask-Script will create help
# documentation using the function's docstring. Try it, and call `python
# manage.py -h` to see the outcome.
manager = Manager(app)

if __name__ == '__main__':
    manager.run()
