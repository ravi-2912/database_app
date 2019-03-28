"""
The flask application package.
"""

from flask import Flask
from flask_wtf.csrf import CsrfProtect

csrf = CsrfProtect()
app = Flask(__name__)
csrf.init_app(app)

import ToughnessDatabase.views
