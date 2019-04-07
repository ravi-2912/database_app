"""
The flask application package.
"""

from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_pymongo import PyMongo

csrf = CSRFProtect()

app = Flask(__name__)
csrf.init_app(app)
session_db = PyMongo(app, uri="mongodb://localhost:27017/session")
toughness_db = PyMongo(app, uri="mongodb://localhost:27017/toughness")

import ToughnessDatabase.views
