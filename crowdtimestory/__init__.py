#!/usr/bin/env python

# crowd time story
# ece695 course project
# Author: Albert, Calvin, Karthik

import sqlite3, os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, send_from_directory, redirect
from werkzeug import secure_filename
from contextlib import closing
#import crowdlib as cl, crowdlib_settings

# configuration
DATABASE = 'crowdtimestory/db/story.db'
DEBUG = True
SECRET_KEY = 'development key'
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

# setup script blueprint
from crowdtimestory.script.views import script 
app.register_blueprint(script)

# setup record blueprint
from crowdtimestory.record.views import record
app.register_blueprint(record)

@app.route('/')
def index():
    return render_template('index.html') 

def connect_db():
    return sqlite3.connect(DATABASE)

# initialize database
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
		
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
