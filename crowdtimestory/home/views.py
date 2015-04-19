import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, Blueprint

from contextlib import closing

home = Blueprint('home', __name__)


@home.route('/')
def index():
    return render_template('home.html', title='Home')