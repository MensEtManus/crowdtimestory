import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, Blueprint, sqlite3
import sys, os
from werkzeug import secure_filename

UPLOAD_FOLDER = "crowdtimestory/static/images/"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


upload = Blueprint('upload', __name__, url_prefix='/upload')


@upload.route('/')
def index():
    return render_template('upload.html', title='Upload')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@upload.route('/upload_image', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        files = request.files.getlist('image_files')
        book_title = secure_filename(request.form['book_title'])
        try:
          con = sqlite3.connect('/db/story.db')
          cursor = con.cursor()
        except sqlite3.Error, e:
          if con:
            con.rollback()
          print "Error %s:" % e.args[0]
        for photo in files:
            if photo and allowed_file(photo.filename):
                filename = secure_filename(photo.filename)
                dir = UPLOAD_FOLDER + book_title
                pic_path = os.path.join(dir, filename)
                try: 
                    if not os.path.exists(dir):
                        os.makedirs(dir)
                except OSError:
                    if not os.path.isdir(dir):
                        raise
                photo.save(os.path.join(dir, filename))
                sql = "INSERT INTO images(title, page, pic_path) VALUES (?,?,?)", (book_title, page, pic_path) 
                cur.execute(sql)
                con.commit()  
        if con:
          con.close()
        return redirect(url_for('home.index'))
    return redirect(url_for('upload.index'))

"""
@upload.route('/upload_image', methods=['GET', 'POST'])
def upload_image(title, page, pic_file):

  if request.method == 'POST':
    with open(pic_file, 'rb') as input_file:
      data = input_file.read()
      binary = sqlite3.Binary(data)
      try:
        con = sqlite3.connect('/db/story.db')
        cursor = con.cursor()
        sql = "INSERT INTO images(title, page, picture) VALUES (?,?,?)", (title, page, binary) 
        cur.execute(sql)
        con.commit()  
      except lite.Error, e:
        if con:
          con.rollback()
        print "Error %s:" % e.args[0]
        sys.exit(1)
      finally:
        if con:
          con.close()
    return redirect(url_for('home.index'))
  return redirect(url_for('upload.index'))
"""
