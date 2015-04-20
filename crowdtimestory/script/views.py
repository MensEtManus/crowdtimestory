from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, Blueprint

script = Blueprint('script', __name__, url_prefix='/script')

@script.route('/')
def index():
    return render_template('script.html', title='script')
