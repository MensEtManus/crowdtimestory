import sqlite3, os
from flask import Flask, request, session, g, redirect, url_for, render_template, send_from_directory, redirect, Blueprint
from werkzeug import secure_filename
#import crowdlib as cl, crowdlib_settings

UPLOAD_FOLDER = 'crowdtimestory/static/audio'
ALLOWED_EXTENSIONS = set(['wav', 'jpg', 'jpge'])

record = Blueprint('record', __name__, url_prefix='/record')

@record.route('/')
def index():
    return 'stage2'

# generate hits for recording voice parts after a script is selected
@record.route('/send_hit_type_2', methods=['GET'])
def send_hit_type_2():
	story = request.args.get('story')
	
	# the total number of characters in the story = the number of HITS to send
	len = g.db.execute('SELECT COUNT(DISTINCT character) FROM stories').fetchall()[0][0]
	
	# a list of all the characters in the story
	parts = g.db.execute('SELECT DISTINCT character FROM stories').fetchall()
	
	# for each character (parts[i][0]) i = 0; i < len; len++) send a hit out with the parameter story and charcter
	
# generate the individual hit template for amt workers
@record.route('/hit_type_2', methods=['GET', 'POST'])
def hit_type_2():
	story = request.args.get('story')
	character = request.args.get('character')
	
	cur = g.db.execute('SELECT page, line_num, script FROM stories WHERE title="' + story + '" AND character = "' + character + '"')
	
	entries = [dict(page=row[0], line=row[1], script=row[2]) for row in cur.fetchall()]
	
	return render_template('hit2.html', entries=entries, story=story, character=character)

# stores the audio file from ajax calls
@record.route('/upload_aud', methods=['POST'])
def upload_aud():
	wav = request.files['wav']
	wav.headers['Content-Type'] = 'audio/wav'
	if wav and allowed_file(wav.filename):
		filename = secure_filename(wav.filename)
		wav.save(os.path.join(UPLOAD_FOLDER, filename))
	return 'file ' + wav.filename + ' stored to server'
	
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS