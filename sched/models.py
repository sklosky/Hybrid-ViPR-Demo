#processing routines for ViPR Hybrid demo app

from datetime import datetime

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship, synonym
from sqlalchemy.ext.declarative import declarative_base
from werkzeug import check_password_hash, generate_password_hash
from flask import Markup

from TwitterAPI import TwitterAPI
import subprocess
import time
import boto
from boto.s3.connection import S3Connection
from boto.s3.key import Key

import os.path

Base = declarative_base()


def run_capture(hashtag):
    result = ''
    
    #Twitter Keys
    #app keys
    twitter1 = 'XwWIvskkKUm6T5gJ3dofNt7lT'
    twitter2 = 'ScSrr6ALpJJVNW9CnegmwFpKceZ3OBLULUeKfcWkpHumsffF2W'
    #user keys
    twitter3 = '901773816-mA5lkLrPlUp5LRj5GisZVz28mJgeXctwSce4cm6u'
    twitter4 = 'BEwO4nxfpTMmH4Pj575nJDPZPiaB2tavngYWyE4k3HUqz'
    
    viprOnline = None

    if (viprOnline):
        print 'initializing ViPR system'

        #Config info to find ViPR in the vLab
        s3secret = 'pBdWy02VWtuB3KuOWvFfJp8tiOCVIQDLvAkrou/p'
        s3user = 'root'
        s3host = '192.168.1.80'
        s3port = 9020
        s3bucket = 'myNewBucket'
        print s3secret
        print s3user
        print s3host

        conn = S3Connection(aws_access_key_id=s3user,
                            aws_secret_access_key=s3secret,
                            host=s3host,
                            port=s3port,
                            calling_format='boto.s3.connection.ProtocolIndependentOrdinaryCallingFormat',
                            is_secure=False)

        print 'Listing all buckets for this user'
        print conn.get_all_buckets()
        mybucket = conn.get_bucket(s3bucket)

    api = TwitterAPI(twitter1, twitter2, twitter3, twitter4)
    r = api.request('search/tweets', {'q':hashtag, 'count':100})
    for item in r.get_iterator():
        result = result + '<p>' + item['text'].encode('ascii', 'ignore') + '</p>'
        result = result + '<p>' + '</p>'
        result = result + '<p>' + item['user']['name'].encode('ascii', 'ignore') + '</p>'
        result = result + '<p>' + '@' + item['user']['screen_name'].encode('ascii', 'ignore') + '</p>'
        if (viprOnline):
            targetstring = '@' + item['user']['screen_name'].encode('ascii', 'ignore') + '\r\n' + item['user']['screen_name'].encode('ascii', 'ignore') + '\r\n' + item['text'].encode('ascii', 'ignore')
            mykey = Key(mybucket)
            mykey.key = '/user/hadoop/input/'
            mykey.key = mykey.key + str(time.time()) + item['user']['screen_name'].encode('ascii', 'ignore') + '.txt'
            mykey.set_contents_from_string(targetstring)

    result = Markup(result)
    return result
    

def run_analyze():
    #run the map reduce scripts on the hadoop system
    #note -- will need to run python as the hadoop user
    result = ''
    myLines = ''

    #check to see if the output file exists
    fname = '/home/hadoop/output.txt'
    if (os.path.isfile(fname)):
        f = open(fname)
        myLines = f.readlines()
        f.close()

    for thisLine in myLines:
        result = result + '<p>' + thisLine + '</p>'
    
    result = Markup(result)
    return (result)

class User(Base):
    """A user login, with credentials and authentication."""
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    name = Column('name', String(200))
    email = Column(String(100), unique=True, nullable=False)
    active = Column(Boolean, default=True)

    _password = Column('password', String(100))

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        if password:
            password = password.strip()
        self._password = generate_password_hash(password)

    password_descriptor = property(_get_password, _set_password)
    password = synonym('_password', descriptor=password_descriptor)

    def check_password(self, password):
        if self.password is None:
            return False
        password = password.strip()
        if not password:
            return False
        return check_password_hash(self.password, password)

    @classmethod
    def authenticate(cls, query, email, password):
        email = email.strip().lower()
        user = query(cls).filter(cls.email==email).first()
        if user is None:
            return None, False
        if not user.active:
            return user, False
        return user, user.check_password(password)

    # Hooks for Flask-Login.
    #
    # As methods, these are only valid for User instances, so the
    # authentication will have already happened in the view functions.
    #
    # If you prefer, you can use Flask-Login's UserMixin to get these methods.

    def get_id(self):
        return str(self.id)

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def __repr__(self):
        return u'<{self.__class__.__name__}: {self.id}>'.format(self=self)

