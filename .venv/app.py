from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/begin')
def begin():
    return render_template('begin.html')




