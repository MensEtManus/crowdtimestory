from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, Blueprint

script = Blueprint('script', __name__, url_prefix='/script')

@script.route('/')
def index():
    return render_template('hit1.html', title='script')
'''
@script.route('script_hit', methods=['GET', 'POST'])
def script_hit():
    return 
  '''
