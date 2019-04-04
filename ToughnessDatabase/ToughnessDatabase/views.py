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

        if len(session["project"]["pipelines"]) == 1:
            return redirect(url_for("add_pipeline_info", line_name=session["project"]["pipelines"][0]["short_name"]))
        else:
            return redirect(url_for("pipelines"))

    return render_template(
        "forms/project.html",
        title = "Add Test Data",
        year = datetime.now().year,
        username = environ["USERNAME"],
        form = form
        )

@app.route("/pipelines")
def pipelines():
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

    if len(session["project"]["pipelines"]) == 1:
        form.go_done.label.text = "Next"
        form.go_cancel.label.text = "Back"
    
    if request.method == "POST" and form.validate_on_submit():
        session["pipelines"] = {
            line_name: {
                "short_name": line_name,
                "line_pipes": [lp for lp in form.line_pipes.data],
                
                "diameter_units": form.diameter_units.data,
                "thickness_units": form.thickness_units.data,
                "length": str(form.length.data),
                "length_units": form.length_units.data,
                
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

        session["pipelines"][line_name]["spools"] = []
        for lp in session["pipelines"][line_name]["line_pipes"]:
            session["pipelines"][line_name]["spools"].append(
                "{d} {du} {t} {tu} {w} {g} {m}".format(
                    d=str(lp["diameter"]),
                    du=session["pipelines"][line_name]["diameter_units"],
                    t=str(lp["thickness"]),
                    tu=session["pipelines"][line_name]["thickness_units"],
                    w=lp["seam_weld_type"],
                    g=lp["grade"],
                    m=lp["manufacturer"],
                ))
        
        if (form.go_done.data):
            if len(session["pipelines"]) == 1:
                if len(session["pipelines"][line_name]["spools"]) == 1:
                    return redirect(url_for("add_test_data", line_name=line_name, spool=session["pipelines"][line_name]["spools"]))
                else:
                    return redirect(url_for("spools"))
            else:
                return (redirect(url_for("pipelines")))
    
        if (form.go_cancel.data):
            session["pipelines"][line_name] = {}
            

    return render_template(
        "forms/pipelineinfo.html",
        title = "Pipeline Data",
        year = datetime.now().year,
        username = environ["USERNAME"],
        line_name=line_name,
        no_lines=len(session["project"]["pipelines"]),
        form = form
        )


@app.route("/spools", methods=["GET", "POST"])
def spools():

    form = {"title": "Pipeline Spools"}
       
    return render_template(
        "forms/spools.html",
        title = "Add Spool Test Data",
        year = datetime.now().year,
        username = environ["USERNAME"],
        pipelines = session["pipelines"],
        form = form
        )



@app.route("/add/<string:line_name>/<string:spool>/test-data", methods=["GET", "POST"])
def add_test_data(line_name, spool):
    """Renders the add test database page layout."""

    """
    try:
        prj = session["tensile_tests"][line_name]
        form = forms.TensileTestForm(request.form, data=prj)
    except:
        form = forms.TensileTestForm(request.form)
    """
    
    form = forms.TestDataForm(request.form)

    if request.method == "POST" and form.validate_on_submit():
        print("POST")
        
        
    return render_template(
        "forms/testdata.html",
        title = "Add Test Data",
        year = datetime.now().year,
        username = environ["USERNAME"],
        line_name = line_name,
        spool = spool,
        form = form
        )