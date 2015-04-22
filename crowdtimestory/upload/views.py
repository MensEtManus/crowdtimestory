import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, Blueprint 
import sys, os
from werkzeug import secure_filename
import re

UPLOAD_FOLDER = "crowdtimestory/static/images/"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


upload = Blueprint('upload', __name__, url_prefix='/upload')


@upload.route('/')
def index():
    return render_template('upload.html', title='Upload')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def get_page_num(photo):
    pattern = r'\d+'
    match = re.search(pattern, photo)
    if match:
        return match.group()



@upload.route('/upload_image', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        files = request.files.getlist('image_files')
        book_title = secure_filename(request.form['book_title'])
        try:
            con = sqlite3.connect('crowdtimestory/db/story.db')
            cursor = con.cursor()
        except sqlite3.Error, e:
            if con:
                con.rollback()
            log.error("Error %s:" % e.args[0])
            con = sqlite3.connect('crowdtimestory/db/story.db')
            cursor = con.cursor()
        except sqlite3.Error, e:
            if con:
                con.rollback()
                print "Error %s:" % e.args[0]
        for photo in files:
            if photo and allowed_file(photo.filename):
                filename = secure_filename(photo.filename)

                # get the page num from the file name
                page = get_page_num(filename)

                dir = UPLOAD_FOLDER + book_title
                pic_path = os.path.join(dir, filename)
                try: 
                    if not os.path.exists(dir):
                        os.makedirs(dir)
                except OSError:
                    if not os.path.isdir(dir):
                        raise
                photo.save(os.path.join(dir, filename))
                cur = con.cursor()
                pic_path = pic_path.replace("crowdtimestory", "..")
                data = [book_title, page, pic_path] 
                sql = "INSERT INTO images(title, page, photo_path) VALUES (?,?,?)" 
                cur.execute(sql, data)
                con.commit()  
        sql = "SELECT page, photo_path FROM images WHERE title = '%s' AND done = 0" % (book_title)
        cur = cur.execute(sql)
        pages = [dict(page=row[0], photo_path=row[1]) for row in cur.fetchall()]
        con.close()
        return render_template('script.html', title='script', story=book_title, pages=pages)
    return redirect(url_for('upload.index'))

