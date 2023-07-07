from flask import Flask
from views import *

app = Flask(__name__)

# Routes
app.add_url_rule('/', view_func=homepage)
app.add_url_rule('/begin', view_func=begin)

if __name__ == '__main__':
    app.run()
