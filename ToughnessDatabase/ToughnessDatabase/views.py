"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, session, \
                  request, jsonify, url_for, \
                  redirect
from ToughnessDatabase import app, forms
from os import environ
from functools import wraps
import itertools
global str

def project_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "project" in session:
            return f(*args, **kwargs)
        else:
            # flash("You need to login first")
            return "Project and pipeline details are required"

    return wrap

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

    try:
        prj = session["project"]
        form = forms.ProjectForm(request.form, data=prj)
    except:
        form = forms.ProjectForm(request.form)
    
    print(form.go_next.data)
    if request.method == "POST" and form.validate_on_submit():
        session["project"] = {
            "name": form.name.data,
            "prj_no": form.prj_no.data,
            "region_prj_no": form.region_prj_no.data,
            "client": form.client.data,
            "prj_type": form.prj_type.data,
            "country": form.country.data,
            "state": form.state.data,
            "city": form.city.data,
            "pipelines": [data for data in form.pipelines.data]            
        }
        session["pipelines"] = {}    
        return redirect(url_for("add_pipeline"))

    return render_template(
        "forms/project.html",
        title = "Add Test Data",
        year = datetime.now().year,
        username = environ["USERNAME"],
        form = form
        )

@app.route("/add/pipeline")
def add_pipeline():
    """Renders the available pipelines."""

    form = {"title": "Pipelines"}
    return render_template(
        "forms/pipeline.html",
        title = "Add Pipeline Information",
        year = datetime.now().year,
        username = environ["USERNAME"],
        pipelines = session["project"]["pipelines"],
        form = form
        )


@app.route("/add/pipeline/<string:line_name>", methods=["GET", "POST"])
def add_pipeline_info(line_name):
    """Renders the add test database page layout."""

    try:
        prj = session["pipelines"][line_name]
        form = forms.PipelineForm(request.form, data=prj)
    except:
        form = forms.PipelineForm(request.form)
    
    form.title += " - {}".format(line_name)

    if request.method == "POST" and form.validate_on_submit():
        session["pipelines"] = {
            line_name: {
                "diameter": [str(dia) for dia in form.diameter.data],
                "diameter_units": form.diameter_units.data,
                "thickness": [str(wt) for wt in form.thickness.data],
                "thickness_units": form.thickness_units.data,
                "length": str(form.length.data),
                "length_units": form.length_units.data,
                
                "grade": [gr for gr in form.grade.data],
                "seam_weld_type": [swt for swt in form.seam_weld_type.data],
                "psl_no": [psl for psl in form.psl_no.data],
                "manufacturer": [man for man in form.manufacturer.data],
                "year_constructed": [yc for yc in form.year_constructed.data],
                
                "design_code": [dc for dc in form.design_code.data],
                "design_press": [str(dp) for dp in form.design_press.data],
                "design_press_units": form.design_press_units.data,
                "design_temp": [str(dt) for dt in form.design_temp.data],
                "design_temp_units": form.design_temp_units.data,
                "design_life": str(form.design_life.data),
                "year_commissioned": str(form.year_commissioned.data),

                "oper_press": [str(op) for op in form.oper_press.data],
                "oper_press_units": form.oper_press_units.data,
                "oper_temp": [str(ot) for ot in form.oper_temp.data],
                "oper_temp_units": form.oper_temp_units.data,

                "test_press": [str(tp) for tp in form.test_press.data],
                "test_press_units": form.test_press_units.data,
                "test_year": str(form.test_year.data)
            }
        }
        
        if (form.go_back.data):
            return (redirect(url_for("add_pipeline")))
        
        #if form.go_next.data and len(session["pipelines"]) == len(session["project"]["pipelines"]):
            #return redirect(url_for('add'))
        #    print("doing")
        #else:
            # TODO: code this up
        #    print("redirecting")
            ##return redirect(url_for('add_pipeline_info', ))
        
    return render_template(
        "forms/pipelineinfo.html",
        title = "Pipeline Data",
        year = datetime.now().year,
        username = environ["USERNAME"],
        line_name=line_name,
        form = form
        )


@app.route("/add/tensile-test/<string:line_name>", methods=["GET", "POST"])
# @project_required
def add_tensile_test(line_name):
    """Renders the add test database page layout."""

    try:
        prj = session["tensile_tests"][line_name]
        form = forms.TensileTestForm(request.form, data=prj)
    except:
        form = forms.TensileTestForm(request.form)
    
    form.title += " - {}".format(line_name)

    if request.method == "POST" and form.validate_on_submit():
        print("POST")
        
        
    return render_template(
        "forms/tensileinfo.html",
        title = "Tensile Test Data",
        year = datetime.now().year,
        username = environ["USERNAME"],
        line_name=line_name,
        form = form
        )