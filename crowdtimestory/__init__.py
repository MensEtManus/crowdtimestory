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
app.config['UPLOAD_FOLDER'] = 'crowdtimestory/static/audio'
app.config['ALLOWED_EXTENSIONS'] = set(['wav', 'jpg', 'jpge'])

# setup home blueprint
from crowdtimestory.home.views import home
app.register_blueprint(home)

# setup upload blueprint
from crowdtimestory.upload.views import upload
app.register_blueprint(upload)


@app.route('/')
def index():
    return render_template('index.html') 

# generate hits for recording voice parts after a script is selected
@app.route('/send_hit_type_2', methods=['GET'])
def send_hit_type_2():
	story = request.args.get('story')
	
	# the total number of characters in the story = the number of HITS to send
	len = g.db.execute('SELECT COUNT(DISTINCT character) FROM stories').fetchall()[0][0]
	
	# a list of all the characters in the story
	parts = g.db.execute('SELECT DISTINCT character FROM stories').fetchall()
	
	# for each character (parts[i][0]) i = 0; i < len; len++) send a hit out with the parameter story and charcter
	
# generate the individual hit template for amt workers
@app.route('/hit_type_2', methods=['GET', 'POST'])
def hit_type_2():
	story = request.args.get('story')
	character = request.args.get('character')
	
	cur = g.db.execute('SELECT page, line_num, script FROM stories WHERE title="' + story + '" AND character = "' + character + '"')
	
	entries = [dict(page=row[0], line=row[1], script=row[2]) for row in cur.fetchall()]
	
	return render_template('hit2.html', entries=entries, story=story, character=character)

# stores the audio file from ajax calls
@app.route('/upload_aud', methods=['POST'])
def upload_aud():
	wav = request.files['wav']
	wav.headers['Content-Type'] = 'audio/wav'
	if wav and allowed_file(wav.filename):
		filename = secure_filename(wav.filename)
		wav.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	return 'file ' + wav.filename + ' stored to server'

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