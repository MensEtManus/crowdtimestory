import sqlite3, os
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, Blueprint

from contextlib import closing

home = Blueprint('home', __name__)

@home.route('/')
def index():

	cur = g.db.execute('SELECT DISTINCT title FROM story ORDER BY title ASC')
	stories = [dict(name=row[0]) for row in cur.fetchall()]
    
	return render_template('home.html', title='Home', stories=stories)