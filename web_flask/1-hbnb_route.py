#!/usr/bin/python3
"""
Python script to start a Flask web application
"""


from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    """Executes when the route / is visited"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    return 'HBNB'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
