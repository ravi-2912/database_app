"""
WT Forms classes for the forms in the Flask application.
"""

from flask_wtf import FlaskForm, Form
from wtforms.fields import StringField, \
        BooleanField, DateTimeField, IntegerField, \
        DecimalField, RadioField, FormField, \
        TextAreaField, SelectField, SubmitField, \
        FormField, FieldList
from wtforms.validators import DataRequired, \
        InputRequired, Optional, NumberRange

class ProjectForm(FlaskForm):
    title = "Project Details"
    name = StringField("Project Name", validators=[DataRequired()])
    prj_no = StringField("Project Number", validators=[DataRequired()])
    region_prj_no = StringField("Regional Project Number", validators=[DataRequired()])

    owner = StringField("Owner(s)")
    operator = StringField("Operator(s)")
    
    country = StringField("Country")
    state = StringField("State")
    city = StringField("City")    
    go_next = SubmitField("Next")
            

class PipelineForm(FlaskForm):
    title = "Pipeline Information"
    name = StringField("Pipeline Name")
    short_name = StringField("Line Name")
    length = DecimalField("Pipeline\"s Length")
    length_units = RadioField("Length Units", choices=[("m", "m"), ("ft", "ft")])

    design_code = FieldList(StringField("Design Code"))
    year_constructed = FieldList(DecimalField("Construction / Commissioning Year"))

    diameter = FieldList(DecimalField("Outer Diameter"))
    diameter_units = RadioField("Diameter Units", choices=[("mm", "mm"), ("inch", "inch")])

    thickness = FieldList(DecimalField("Wall Thickness"))
    thickness_units = RadioField("Thickness Units", choices=[("mm", "mm"), ("inch", "inch")])
    
    grade = FieldList(SelectField("Material Grade"))
    seam_Weld_type = FieldList(SelectField("Weld Type"))
    psl_no = FieldList(SelectField("Product Specification Level (PSL)", choices=[("PSL1", "PSL 1"), ("PSL2", "PSL 2")]))
    manufacturer = FieldList(StringField("Pipe Manufacturer"))

    presure = FieldList(DecimalField("Design / Operating Pressure"))
    press_units = RadioField("Pressure Units", choices=[("bar", "bar"), ("psi", "psi")])

    test_pres = FieldList(DecimalField("Test Pressure"))
    test_press_units = RadioField("Test Pressure Units", choices=[("bar", "bar"), ("psi", "psi")])

    temp = FieldList(DecimalField("Design / Operating Temperatures"))
    temp_units = RadioField("Temperature Units", choices=[("C", "°C"), ("F", "°F")])

    go_next = SubmitField("Next")