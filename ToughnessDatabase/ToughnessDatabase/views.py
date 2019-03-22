"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, session, request
from ToughnessDatabase import app, forms
from os import environ

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
        username=environ["USERNAME"]
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        username=environ["USERNAME"],
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        username=environ["USERNAME"],
        message='Your application description page.'
    )

@app.route('/add_to_db/<page_name>', methods=['GET', 'POST', 'PUT'])
def add_to_db(page_name):
    """Renders the add test database page layout."""




    default_page_name = 'default.html'
    form = {'title': "Add Test Data to Database"}

    if page_name == 'projectdetails.html':
        form = forms.ProjectForm()
    if page_name == "pipelineinfo.html":
        form = forms.PipelineForm()      
        
    return render_template(
        'forms/{}'.format(page_name),
        title = 'Add Test Data',
        year = datetime.now().year,
        username=environ["USERNAME"],
        form = form
    )