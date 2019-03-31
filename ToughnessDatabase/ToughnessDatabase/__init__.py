"""
The flask application package.
"""

from flask import Flask
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()

app = Flask(__name__)
csrf.init_app(app)

import ToughnessDatabase.views
