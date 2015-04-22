from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, Blueprint
import logging
import crowdlib as cl, crowdlib_settings, time

script = Blueprint('script', __name__, url_prefix='/script')


hit_type = cl.create_hit_type(
  title       = "Please extract scripts from the picture",
  description = "Identify the characters in this picture, add corresponding script for each character",
  reward      = 0.5
)

@script.route('/')
def index():
    book_title = "test"
    pic_path = "../static/images/1.jpg"
    return render_template('hit1.html', title='script', book_title=book_title, pic_path=pic_path)

@script.route('/script_result', methods=['GET', 'POST'])
def script_hit():
    if request.method == "POST": 
        f = request.form
        logging.warn(len(f))
        logging.warn("start loggin")
        for key in f.keys():
            for value in f.getlist(key):
                string = key + ":" + value
                logging.warn(string)
        logging.warn("logging end")

    return redirect(url_for('home.index'))

# generate the individual hit template for amt workers
@script.route('/hit_type_1', methods=['GET', 'POST'])
def hit_type_1():
    story = request.args.get('story')
    character = request.args.get('character')
    assignmentId = request.args.get('assignmentId')
    turkSubmitTo = request.args.get("turkSubmitTo")
    
    cur = g.db.execute('SELECT page, line_num, script FROM story WHERE title="' + story + '" AND character = "' + character + '"')
    
    entries = [dict(page=row[0], line=row[1], script=row[2]) for row in cur.fetchall()]
    
    return render_template('hit1.html', pic_path=pic_path, book_title=book_title, assignmentId=assignmentId, turkSubmitTo=turkSubmitTo)

# stores the scripts for stories from ajax calls
@script.route('/upload_script', methods=['POST'])
def upload_aud():
    global AUD_SUBMITTED
    # TODO save scripts from the HIT to database
    
    return 'success'

# check if the HITS are done
@script.route('/check_results', methods=['POST'])
def check_results():
    if AUD_SUBMITTED == HITS_SENT:
        return 'done'
    else:   
        return 'waiting for ' + str(HITS_SENT - PIC_SUBMITTED) + ' more hits to be completed'


@script.route('/cancelHIT', methods=['GET'])
def cancelHIT():
    cl.set_all_hits_unavailable()
    return 'HIT has been cancelled'