"""
This script runs the ToughnessDatabase application using a development server.
"""

from os import environ, urandom
from ToughnessDatabase import app

SECRET_KEY = urandom(32)

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555

    app.debug = True
    app.config['SECRET_KEY'] = SECRET_KEY
    app.run(HOST, PORT)
