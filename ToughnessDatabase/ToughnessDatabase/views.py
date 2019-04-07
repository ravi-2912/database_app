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
from bson.json_util import loads, dumps

session = session_db.db
project = session["project"]
pipelines = session["pipelines"]
test_data = session["test_data"]
exclude = {"_id": 0, "csrf_token": 0, "go_next": 0}

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
    try:
        project.delete_many({})
        pipelines.delete_many({})
        test_data.delete_many({})
    except: 
        pass

    form = {"title": "Add Test Data to Toughness Database"}
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

    if request.method == "POST" and form.validate_on_submit():
        prj_pipelines = [x for x in project.find_one()["pipelines"]]
        session_pipelines = [x for x in pipelines.find({}, {"_id": 0, "short_name": 1, "spools": 1})]
        
        if len(prj_pipelines) == len(session_pipelines):
            return redirect(url_for("spools"))
        else:
            line_names_available = [x["short_name"] for x in prj_pipelines]
            line_names_with_data = [x["short_name"] for x in session_pipelines]
            unfilled_line_names = list(set(line_names_available) ^ set(line_names_with_data))
            if len(unfilled_line_names) > 0:
                return redirect(url_for("add_pipeline_info", line_name=unfilled_line_names[0]))
            else: 
                return redirect(url_for("spools"))
    
        
    
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
                "{d}_{du}_{t}_{tu}_{w}_{g}_{m}".format(
                    d = lp["diameter"],
                    du = pipeline["diameter_units"],
                    t = lp["thickness"],
                    tu = pipeline["thickness_units"],
                    w = lp["seam_weld_type"],
                    g = lp["grade"],
                    m = lp["manufacturer"],
                ))
        pprint(spools)
        pipeline["spools"] = spools
        pipeline["short_name"] = line_name
        
        pipelines.insert_one(pipeline)
        
        if (form.go_next.data):
            # refactor all conditions below
            prj_pipelines = [x for x in project.find_one()["pipelines"]]
            session_pipelines = [x for x in pipelines.find({}, exclude)]
            if len(prj_pipelines) == 1 and len(spools) == 1:
                return redirect(url_for("add_test_data", line_name=line_name, spool=spools[0]))
            
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
    class SpoolsListForm(FlaskForm):
        title = "Pipeline Spools"
        go_next = SubmitField("Next")

    form = SpoolsListForm()
    
    existing_test = [x["short_name"]+"_"+x["spool"] for x in test_data.find({}, {"_id": 0, "short_name": 1, "spool": 1})]
    available_spools = [x for x in pipelines.find({}, {"_id": 0, "short_name": 1, "spools": 1})]
    x = []
    for p in available_spools:
        for s in p["spools"]:
            x.append(p["short_name"]+"_"+s)
    available_spools = x
    
    if len(existing_test) == len(available_spools):
        form.go_next.label.text = "Review and Submit"
    
    if request.method == "POST" and form.validate_on_submit():
        existing_test = [x["short_name"]+"_"+x["spool"] for x in test_data.find({}, {"_id": 0, "short_name": 1, "spool": 1})]
        remaining_test = list(set(available_spools) ^ set(existing_test))
        if len(existing_test) == len(available_spools):
            return redirect(url_for("review_submit"))
        
        if len(remaining_test) > 0:
            spool = remaining_test[0]
            line_name, spool = spool.split("_", 1)
            return redirect(url_for("add_test_data", line_name=line_name, spool=spool))
            
        return dumps(available_spools)
    

    return render_template(
        "forms/spools.html",
        title = "Add Spool Test Data",
        year = datetime.now().year,
        username = environ["USERNAME"],
        pipelines = [x for x in pipelines.find({},{"short_name": 1, "spools": 1, "name": 1, "_id":0})],
        form = form
        )



@app.route("/add/<string:line_name>/<string:spool>/test-data", methods=["GET", "POST"])
def add_test_data(line_name, spool):
    """Renders the add test database page layout."""

    try:
        data = test_data.find_one({"short_name": line_name, "spool": spool})
        form = forms.TestDataForm(data=data)
        pprint(data)
    except:
        form = forms.TestDataForm()
        print("No")
    
    
    form.title += " - {} - {}".format(line_name, spool.replace("_"," "))
    existing_test = [x["short_name"]+"_"+x["spool"] for x in test_data.find({}, {"_id": 0, "short_name": 1, "spool": 1})]
    available_spools = [x for x in pipelines.find({}, {"_id": 0, "short_name": 1, "spools": 1})]

    if len(existing_test) == len(available_spools):
        form.go_next.label.text = "Review and Submit"

    if request.method == "POST" and form.validate_on_submit():
        test_data.delete_many({"short_name": line_name, "spool": spool})
        test = form.data
        test["short_name"] = line_name
        test["spool"] = spool
        test_data.insert_one(test)


        if form.go_next.data:
            existing_test = [x["short_name"]+"_"+x["spool"] for x in test_data.find({}, {"_id": 0, "short_name": 1, "spool": 1})]
            x = []
            for p in available_spools:
                for s in p["spools"]:
                    x.append(p["short_name"]+"_"+s)
            available_spools = x
            remaining_test = list(set(available_spools) ^ set(existing_test))

            if len(existing_test) == len(available_spools):
                return redirect(url_for("review_submit"))
            
            if len(remaining_test) > 0:
                spool = remaining_test[0]
                line_name, spool = spool.split("_", 1)
                return redirect(url_for("add_test_data", line_name=line_name, spool=spool)) 
                
    return render_template(
        "forms/testdata.html",
        title = "Add Test Data",
        year = datetime.now().year,
        username = environ["USERNAME"],
        line_name = line_name,
        spool = spool,
        no_lines = len(project.find_one()["pipelines"]),
        no_spools = len(available_spools),
        form = form
        )


@app.route("/review", methods=["GET", "POST"])
def review_submit():

    class ReviewSubmitForm(FlaskForm):
        title = "Review and Submit"
        start_again = SubmitField("Start Again")
        submit_to_db = SubmitField("Submit to DB")

    form = ReviewSubmitForm()
    
    if request.method == "POST" and form.validate_on_submit():
        if form.start_again.data:
            return redirect(url_for('add'))
        
        if form.submit_to_db.data:
            return "SUBMITED"

    return render_template(
        "forms/review.html",
        title = form.title,
        year = datetime.now().year,
        username = environ["USERNAME"],
        project = dumps(project.find_one({}, exclude)),
        pipelines = dumps(pipelines.find({}, exclude)),
        test_data = dumps(test_data.find({}, exclude)),
        form = form
    )