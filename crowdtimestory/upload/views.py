import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, Blueprint
import sys

upload = Blueprint('upload', __name__, url_prefix='/upload')


@upload.route('/')
def index():
    return render_template('upload.html', title='Upload')

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
