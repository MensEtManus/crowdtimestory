from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, Blueprint
import logging
import crowdlib as cl, crowdlib_settings, time
import json

script = Blueprint('script', __name__, url_prefix='/script')


hit_type = cl.create_hit_type(
  title       = "Please extract scripts from the picture",
  description = "Identify the characters in this picture, add corresponding script for each character",
  reward      = 0.5
)

@script.route('/')
def index():
    book_title = "test"
    photo_path = "../static/images/1.jpg"
    page_num = 1
    return render_template('hit1.html', title='script', book_title=book_title, photo_path=photo_path, page_num=page_num)

@script.route('/script_result', methods=['GET', 'POST'])
def script_hit():
    if request.method == "POST": 
        f = request.form
        logging.warn(len(f))
        logging.warn("start loggin")
        
        characters = f.getlist("character")
        texts = f.getlist("text")
        for i in range(0, len(characters)):
            string = "character " + str(i) + ": " + characters[i]
            logging.warn(string)
            string = "text " + str(i) + ": " + texts[i]
            logging.warn(string)
       
        '''    
        for key in f.keys():
            for value in f.getlist(key):
                string = key + ":" + value
                logging.warn(string)
        '''
        logging.warn("logging end")

    return redirect(url_for('home.index'))

# generate hits for extracting scripts from a page of a book
@script.route('/send_hit_type_1', methods=['POST'])
def send_hit_type_1():
    global HITS_SENT

    story = request.args.get('story')
    
    # select all the pages that are not scripted in the story
    pages = g.db.execute('SELECT page FROM images WHERE title="' + story +'" AND done=0').fetchall()

    # the number of HITS SENT == number of pages that are not scripted
    num_of_pages = len(pages)
    HITS_SENT = num_of_pages
    logging.warn("page number????")
    logging.warn(pages[0])
    # for each character (parts[i][0]) i = 0; i < len; len++) send a hit out with the parameter story and charcter
    for x in range(0, num_of_pages):
        hit = hit_type.create_hit(
          url = "https://128.46.32.82:8011/script/hit_type_1?story=" + story + "&page=" + pages[x][0],
          height = 800
        )
    
    return 'Workers are working hard to extract scripts from the pictures, please wait patiently'

# generate the individual hit template for amt workers
@script.route('/hit_type_1', methods=['GET', 'POST'])
def hit_type_1():
    book_title = request.args.get('book_title')
    page_num = request.args.get('page')
    assignmentId = request.args.get('assignmentId')
    turkSubmitTo = request.args.get("turkSubmitTo")
    
    
    return render_template('hit1.html', photo_path=photo_path, page_num=page_num, book_title=book_title, assignmentId=assignmentId, turkSubmitTo=turkSubmitTo)

# stores the scripts for stories from ajax calls
@script.route('/upload_script', methods=['GET','POST'])
def upload_script():
    global HITS_SUBMITTED
    page_num = request.args.get('page')
    story = request.args.get('book_title')
    # TODO save scripts from the HIT to database
    if request.method == "POST": 

        data = json.loads(request.get_json())

        #page_num = f.get('page_num')
        #story = f.get('book_title')
        characters = data['character']
        texts = data['text']

        logging.warn("start loggin")
        logging.warn(page_num)
        logging.warn(story)

        for i in range(0, len(characters)):
            string = "character " + str(i) + ": " + characters[i]
            logging.warn(string)
            string = "text " + str(i) + ": " + texts[i]
            logging.warn(string)
    HITS_SUBMITTED = HITS_SUBMITTED + 1
    return 'success'

# check if the HITS are done
@script.route('/check_results', methods=['POST'])
def check_results():
    if HITS_SUBMITTED == HITS_SENT:
        return 'done'
    else:   
        return 'waiting for ' + str(HITS_SENT - HITS_SUBMITTED) + ' more hits to be completed'


@script.route('/cancelHIT', methods=['GET'])
def cancelHIT():
    cl.set_all_hits_unavailable()
    return 'HIT has been cancelled'