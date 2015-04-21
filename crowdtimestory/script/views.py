from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, Blueprint
import logging

script = Blueprint('script', __name__, url_prefix='/script')

@script.route('/')
def index():
    book_title = "test"
    return render_template('hit1.html', title='script', book_title=book_title)

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
