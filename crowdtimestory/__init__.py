#!/usr/bin/env python

# crowd time story
# ece695 course project
# Author: Albert, Calvin, Karthik

from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash



# create the application
app = Flask(__name__)

# wtf secret key??
app.secret_key = "420blazeityoloswagfuck"



# setup home blueprint
from crowdtimestory.home.views import home
app.register_blueprint(home)

# setup upload blueprint
from crowdtimestory.upload.views import upload
app.register_blueprint(upload)


@app.route('/')
def index():
    return render_template('index.html') 



