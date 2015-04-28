from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, Blueprint
import logging
import crowdlib as cl, crowdlib_settings, time
import json
import sqlite3 

script = Blueprint('script', __name__, url_prefix='/script')


hit_type = cl.create_hit_type(
  title       = "Please extract scripts from the picture",
  description = "Identify the characters in this picture, add corresponding script for each character",
  reward      = 0.5
)

HITS_SUBMITTED = 0
HITS_SENT = 0

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
    pages = g.db.execute('SELECT DISTINCT page, photo_path FROM images WHERE title="' + story +'" AND done=0').fetchall()

    # the number of HITS SENT == number of pages that are not scripted
    num_of_pages = len(pages)
    HITS_SENT = HITS_SENT + num_of_pages

    for page in pages:
        page_num = str(page[0])
        hit = hit_type.create_hit(
          url = "https://128.46.32.82:8012/script/hit_type_1?story=" + story + "&page=" + page_num + "&photo_path=" + page[1],
          height = 800
        )
    
    return 'Workers are working hard to extract scripts from the pictures, please wait patiently'

# generate the individual hit template for amt workers
@script.route('/hit_type_1', methods=['GET', 'POST'])
def hit_type_1():
    book_title = request.args.get('story')
    page_num = request.args.get('page')
    photo_path = request.args.get('photo_path')
    assignmentId = request.args.get('assignmentId')
    turkSubmitTo = request.args.get("turkSubmitTo")
    
    
    return render_template('hit1.html', photo_path=photo_path, page_num=page_num, book_title=book_title, assignmentId=assignmentId, turkSubmitTo=turkSubmitTo)

# stores the scripts for stories from ajax calls
@script.route('/upload_script', methods=['GET','POST'])
def upload_script():
    global HITS_SUBMITTED 
    page_num = request.args.get('page')
    try:
        con = sqlite3.connect('crowdtimestory/db/story.db')
        cur = con.cursor()
    except sqlite3.Error, e:
        if con:
            con.rollback()
        log.error("Error %s:" % e.args[0])

    # TODO save scripts from the HIT to database
    if request.method == "POST": 

        story = request.json['story']
        page_num = request.json['page']
        
        characters = request.json['characters']
        texts = request.json['texts']

        logging.warn("start loggin")
        logging.warn(page_num)
        logging.warn(story)

        for i in range(0, len(characters)):
            line_num = i + 1
            character = characters[i]
            script = texts[i]
            info = [story, page_num, line_num, character, script]
        
            sql = "INSERT INTO story(title, page, line_num, character, script) VALUES (?,?,?,?,?)" 

            cur.execute(sql, info)
            con.commit()  

        # update the done infomation in the images table for the page of a book
        sql_update_images = "UPDATE images SET done = %d WHERE title = '%s' AND page = %d" % (1, story, page_num)
        cur.execute(sql_update_images)
        con.commit()

    con.close()
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