import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, Blueprint

from contextlib import closing

upload = Blueprint('upload', __name__, url_prefix='/upload')

# configuration
DATABASE = './db/story.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


@upload.route('/')
def index():
    return render_template('upload.html', title='Upload')

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
