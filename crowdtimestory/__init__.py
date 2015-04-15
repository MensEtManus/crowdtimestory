#!/usr/bin/env python

# crowd time story
# ece695 course project
# Author: Albert, Calvin, Karthik

import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash


from contextlib import closing


# configuration
DATABASE = './db/story.db'
DEBUG = True
# SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create the application
app = Flask(__name__)

# wtf secret key??
app.secret_key = "420blazeityoloswagfuck"


app.config.from_object(__name__)


# setup home blueprint
from crowdtimestory.home.views import home
app.register_blueprint(home)

# setup upload blueprint
from crowdtimestory.upload.views import upload
app.register_blueprint(upload)


@app.route('/')
def index():
    return render_template('index.html') 

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

# initialize database
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@upload.before_request
def before_request():
    g.db = connect_db()

@upload.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
