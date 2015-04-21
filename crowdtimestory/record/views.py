import sqlite3, os
from flask import Flask, request, session, g, redirect, url_for, render_template, send_from_directory, redirect, Blueprint
from werkzeug import secure_filename
import crowdlib as cl, crowdlib_settings, time

UPLOAD_FOLDER = 'crowdtimestory/static/audio'
ALLOWED_EXTENSIONS = set(['wav', 'jpg', 'jpge'])
HITS_SENT = 0;
AUD_SUBMITTED = 0;

record = Blueprint('record', __name__, url_prefix='/record')

hit_type = cl.create_hit_type(
  title       = "Record voice parts for audio book.",
  description = "Record the script for your character",
  reward      = 0.5
)

#index page that displays script for approval before sending scripts out for voice recording.
@record.route('/')
def index():
	story = request.args.get('story')
	cur = g.db.execute('SELECT character, script FROM story WHERE title = "' + story + '"')
	entries = [dict(character=row[0], script=row[1]) for row in cur.fetchall()]
	
	return render_template('record.html', story=story, entries=entries)

# generate hits for recording voice parts after a script is selected
@record.route('/send_hit_type_2', methods=['POST'])
def send_hit_type_2():
	global HITS_SENT

	story = request.args.get('story')
	
	# the total number of characters in the story = the number of HITS to send
	len = g.db.execute('SELECT COUNT(DISTINCT character) FROM story').fetchall()[0][0]
	
	# the total number of lines in the story = the number of AUD to receive
	aud_len = g.db.execute('SELECT COUNT(*) FROM story').fetchall()[0][0]
	HITS_SENT = HITS_SENT + aud_len
	
	# a list of all the characters in the story
	parts = g.db.execute('SELECT DISTINCT character FROM story').fetchall()
	
	# for each character (parts[i][0]) i = 0; i < len; len++) send a hit out with the parameter story and charcter
	for x in range(0, len):
		hit = hit_type.create_hit(
		  url = "https://128.46.32.82:8012/record/hit_type_2?story=" + story + "&character=" + parts[x][0],
		  height = 800
		)
	
	return 'your audio book is being created at this moment, please wait patiently'
	
# generate the individual hit template for amt workers
@record.route('/hit_type_2', methods=['GET', 'POST'])
def hit_type_2():
	story = request.args.get('story')
	character = request.args.get('character')
	assignmentId = request.args.get('assignmentId')
	turkSubmitTo = request.args.get("turkSubmitTo")
	
	cur = g.db.execute('SELECT page, line_num, script FROM story WHERE title="' + story + '" AND character = "' + character + '"')
	
	entries = [dict(page=row[0], line=row[1], script=row[2]) for row in cur.fetchall()]
	
	return render_template('hit2.html', entries=entries, story=story, character=character, assignmentId=assignmentId, turkSubmitTo=turkSubmitTo)

# stores the audio file from ajax calls
@record.route('/upload_aud', methods=['POST'])
def upload_aud():
	global AUD_SUBMITTED
	AUD_SUBMITTED = AUD_SUBMITTED + 1

	wav = request.files['wav']
	wav.headers['Content-Type'] = 'audio/wav'
	if wav and allowed_file(wav.filename):
		filename = secure_filename(wav.filename)
		wav.save(os.path.join(UPLOAD_FOLDER, filename))
	return 'success'

# check if the HITS are done
@record.route('/check_results', methods=['POST'])
def check_results():
	if AUD_SUBMITTED == HITS_SENT:
		return 'done'
	else:	
		return 'waiting for ' + str(HITS_SENT - AUD_SUBMITTED) + ' more recordings to be completed'
	
# displays final result
@record.route('/result', methods=['GET'])
def result():
	story = request.args.get('story')
	
	pages = g.db.execute('SELECT COUNT(DISTINCT page) FROM story').fetchall()[0][0]
	
	cur = g.db.execute('SELECT page, line_num FROM story WHERE title="' + story +'"')
	entries = [dict(page=row[0], line=row[1]) for row in cur.fetchall()]
	
	return render_template('result.html', story=story, pages=pages, entries=entries)
	
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
	
# functions for testing AMT:
@record.route('/sendHIT', methods=['GET'])
def sendHIT():
	hit = hit_type.create_hit(
	  url = "https://128.46.32.82:8012/record/hit_type_2?story=Where%20the%20wild%20things%20are&character=mother",
	  height = 300
	)
	return 'HIT has been sent'

@record.route('/cancelHIT', methods=['GET'])
def cancelHIT():
	cl.set_all_hits_unavailable()
	return 'HIT has been cancelled'