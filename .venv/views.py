from flask import render_template

def homepage():
    return render_template('home.html')

def begin():
    return render_template('begin.html')