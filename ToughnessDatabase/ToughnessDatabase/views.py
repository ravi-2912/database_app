"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, session as liogin_session, \
                  request, jsonify, url_for, \
                  redirect, g
from ToughnessDatabase import app, forms, session_db
from os import environ
from functools import wraps
import itertools
from pprint import pprint
from flask_wtf import FlaskForm
from wtforms import SubmitField

session = session_db.db
project = session["project"]
pipelines = session["pipelines"]
test_data = session["test_data"]


@app.route("/")
@app.route("/home")
def home():
    """Renders the home page."""
    
    return render_template(
        "index.html",
        title="Home Page",
        year=datetime.now().year,
        username=environ["USERNAME"]
    )

@app.route("/contact")
def contact():
    """Renders the contact page."""
    return render_template(
        "contact.html",
        title="Contact",
        year=datetime.now().year,
        username=environ["USERNAME"],
        message="Your contact page."
    )


@app.route("/ext/about")
def about():
    """Renders the about page."""
    return render_template(
        "about.html",
        title="About",
        year=datetime.now().year,
        username=environ["USERNAME"],
        message="Your application description page."
    )


@app.route("/add", methods=["GET", "POST", "PUT", "DELETE"])
def add():
    """Renders the add test database page layout."""
    form = {"title": "Add Test Data"}
    return render_template(
        "add.html",
        title = "Add Test Data",
        year = datetime.now().year,
        username=environ["USERNAME"],
        form = form
        )


@app.route("/add/project", methods=["GET", "POST"])
def add_project():
    """Renders the add test database page layout."""
    
    testdata = {
        "name": "TEST PROJECT",
        "prj_no": "12345-56789-0123",
        "region_prj_no": "12345-98",
        "client": "",
        "prj_type": "",
        "country": "",
        "state": "",
        "city": "",
        "pipelines":[
            {
                "short_name": "P01",
                "name": ""
            },{
                "short_name": "P02",
                "name": ""
            },{
                "short_name": "P03",
                "name": ""
            }
        ]
    }

    
    try:
        form = forms.ProjectForm(data=testdata)
    except:
        form = forms.ProjectForm()
    
    if request.method == "POST" and form.validate_on_submit():
        project.delete_many({})
        project.insert_one(form.data)
        prj = project.find_one()        
        if len(prj["pipelines"]) == 1:
            return redirect(url_for("add_pipeline_info", line_name=prj["pipelines"][0]["short_name"]))
        else:
            return redirect(url_for("show_pipelines"))

    return render_template(
        "forms/project.html",
        title = "Add Test Data",
        year = datetime.now().year,
        username = environ["USERNAME"],
        form = form
        )

@app.route("/pipelines", methods=["GET", "POST"])
def show_pipelines():
    """Renders the available pipelines."""

    class PipelinesTableForm(FlaskForm):
        title = "Pipelines"
        go_next = SubmitField("Next")
    
    form = PipelinesTableForm()

    if request.method == "POST":
        prj_pipelines = [x for x in project.find_one()["pipelines"]]
        session_pipelines = [x for x in pipelines.find({}, {"_id": 0, "short_name": 1, "spools": 1})]
        
        if len(prj_pipelines) == len(session_pipelines):
            return redirect(url_for('spools'))
        
    
    
    return render_template(
        "forms/pipeline.html",
        title = "Add Pipeline Information",
        year = datetime.now().year,
        username = environ["USERNAME"],
        pipelines = project.find_one()["pipelines"],
        form = form
        )



@app.route("/add/pipeline/<string:line_name>", methods=["GET", "POST"])
def add_pipeline_info(line_name):
    """Renders the add test database page layout."""

    try:
        data = pipelines.find_one({"short_name": line_name})
        form = forms.PipelineForm(data=data)
    except:
        form = forms.PipelineForm()
    
    form.title += " - {}".format(line_name)
    
    

    if request.method == "POST" and form.validate_on_submit():
        pipelines.delete_many({"short_name": line_name})
        pipeline = form.data
        spools = []
        
        for lp in pipeline["line_pipes"]:
            spools.append(
                "{d} {du} {t} {tu} {w} {g} {m}".format(
                    d = lp["diameter"],
                    du = pipeline["diameter_units"],
                    t = lp["thickness"],
                    tu = pipeline["thickness_units"],
                    w = lp["seam_weld_type"],
                    g = lp["grade"],
                    m = lp["manufacturer"],
                ))
        
        pipeline["spools"] = spools
        pipeline["short_name"] = line_name
        
        pipelines.insert_one(pipeline)
        
        if (form.go_next.data):
            # refactor all conditions below
            prj_pipelines = [x for x in project.find_one()["pipelines"]]
            session_pipelines = [x for x in pipelines.find({}, {"_id": 0, "short_name": 1})]
            if len(prj_pipelines) == 1 and len(spools) == 1:
                return redirect(url_for("add_test_data", line_name=line_name, spool=spools))
            
            if len(prj_pipelines) == 1 and len(spools) > 1:
                return redirect(url_for("spools"))
            
            if len(prj_pipelines) > 1:
                line_names_available = [x["short_name"] for x in prj_pipelines]
                line_names_with_data = [x["short_name"] for x in session_pipelines]
                unfilled_line_names = list(set(line_names_available) ^ set(line_names_with_data))
                if len(unfilled_line_names) > 0:
                    return redirect(url_for("add_pipeline_info", line_name=unfilled_line_names[0]))
                else: 
                    return redirect(url_for("spools"))          
            
            

    return render_template(
        "forms/pipelineinfo.html",
        title = "Pipeline Data",
        year = datetime.now().year,
        username = environ["USERNAME"],
        line_name=line_name,
        no_lines=len(project.find_one()["pipelines"]),
        form = form
        )


@app.route("/spools", methods=["GET", "POST"])
def spools():

    form = {"title": "Pipeline Spools"}
    pprint([x for x in pipelines.find({},{"short_name": 1, "spools": 1})])
    return render_template(
        "forms/spools.html",
        title = "Add Spool Test Data",
        year = datetime.now().year,
        username = environ["USERNAME"],
        pipelines = [x for x in pipelines.find({},{"short_name": 1, "spools": 1, "name": 1})["spools"]],
        form = form
        )



@app.route("/add/<string:line_name>/<string:spool>/test-data", methods=["GET", "POST"])
def add_test_data(line_name, spool):
    """Renders the add test database page layout."""

    try:
        form = forms.TestDataForm(data=session["test-data"][line_name][spool])
    except:
        form = forms.TestDataForm()
    
    
    form.title += " - {} - {}".format(line_name, spool)

    if request.method == "POST" and form.validate_on_submit():
        test_data.delete_many({"short_name": line_name, "spool": spool})
        test = form.data
        test["short_name"] = line_name
        test["spool"] = spool
        test_data.insert_one(test)

        if form.go_next.data:
            redirect(url_for("spools"))
        
    pprint(pipelines.find({"short_name": line_name}, {"spools":1}))
    
    return render_template(
        "forms/testdata.html",
        title = "Add Test Data",
        year = datetime.now().year,
        username = environ["USERNAME"],
        line_name = line_name,
        spool = spool,
        no_lines = len(project.find_one()["pipelines"]),
        no_spools = len([x for x in pipelines.find({"short_name": line_name}, {"spools":1, "_id":0})]),
        form = form
        )


@app.route("/review", methods=["GET", "POST"])
def review_submit():
    return "done"