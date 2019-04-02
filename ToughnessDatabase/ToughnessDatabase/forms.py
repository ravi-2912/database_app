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


class PipelineNameListForm(FlaskForm):
    class Meta:
        csrf = False
    
    short_name = StringField("Line Name", validators=[DataRequired()])
    name = StringField("Pipeline Full Name")


class ProjectForm(FlaskForm):
    title = "Project Details"
    name = StringField("Project Name", validators=[DataRequired()])
    prj_no = StringField("Project Number", validators=[DataRequired()])
    region_prj_no = StringField("Regional Project Number", validators=[DataRequired()])
    client = StringField("Client(s) Names")
    prj_type = StringField("Type of project,assessment, etc.")
    country = StringField("Country")
    state = StringField("State")
    city = StringField("City")
    pipelines = FieldList(FormField(PipelineNameListForm), min_entries=1)
    go_next = SubmitField("Next")


class PipelineForm(FlaskForm):
    title = "Pipeline Information"
    
    diameter = FieldList(DecimalField("Outer Diameter"), min_entries=1, validators=[Optional()])
    diameter_units = RadioField("Diameter Units", choices=[("mm", "mm"), ("inch", "inch")], validators=[Optional()])
    thickness = FieldList(DecimalField("Wall Thickness"), min_entries=1, validators=[Optional()])
    thickness_units = RadioField("Thickness Units", choices=[("mm", "mm"), ("inch", "inch")], validators=[Optional()])
    length = DecimalField("Pipeline Length", validators=[Optional()])
    length_units = RadioField("Length Units", choices=[("m", "m"), ("ft", "ft")], validators=[Optional()])
    
    grade = FieldList(SelectField("Material Grade", choices=[("",""), ("b", "Grade B"), ("X42", "Grade X42"), ("X52", "Grade X52")]), min_entries=1)
    seam_weld_type = FieldList(SelectField("Weld Type", choices=[("",""), ("DSAW", "DSAW"), ("EFW", "EFW"), ("ERW", "ERW"), ("SMLS", "SMLS")]), validators=[Optional()], min_entries=1)
    psl_no = FieldList(SelectField("Product Specification Level (PSL)", choices=[("",""), ("PSL1", "PSL 1"), ("PSL2", "PSL 2")]), validators=[Optional()], max_entries=2, min_entries=1)
    manufacturer = FieldList(StringField("ManufacturerName"), min_entries=1, validators=[Optional()])
    year_constructed = FieldList(DecimalField("Construction Year"), validators=[Optional()], min_entries=1)
    
    design_code = FieldList(StringField("Design Code"), min_entries=1)
    design_press = FieldList(DecimalField("Design Pressure"), validators=[Optional()], min_entries=1)
    design_press_units = RadioField("Pressure Units", choices=[("bar", "bar"), ("psi", "psi")], validators=[Optional()])
    design_temp = FieldList(DecimalField("Design Temperatures"), validators=[Optional()], min_entries=1)
    design_temp_units = RadioField("Temperature Units", choices=[("C", "°C"), ("F", "°F")], validators=[Optional()])
    design_life = DecimalField("Design Life in Years", validators=[Optional()])
    year_commissioned = DecimalField("Commissioning Year", validators=[Optional()])

    oper_press = FieldList(DecimalField("Operating Pressure"), validators=[Optional()], min_entries=1)
    oper_press_units = RadioField("Pressure Units", choices=[("bar", "bar"), ("psi", "psi")], validators=[Optional()])
    oper_temp = FieldList(DecimalField("Operating Temperatures"), validators=[Optional()], min_entries=1)
    oper_temp_units = RadioField("Temperature Units", choices=[("C", "°C"), ("F", "°F")], validators=[Optional()])

    test_press = FieldList(DecimalField("Test Pressure"), validators=[Optional()], min_entries=1)
    test_press_units = RadioField("Test Pressure Units", choices=[("bar", "bar"), ("psi", "psi")], validators=[Optional()])
    test_year = DecimalField("Test Year", validators=[Optional()])
    
    go_cancel = SubmitField("Cancel")
    go_done = SubmitField("Done")

class TensileForm(FlaskForm):
    class Meta:
        csrf = False

    yields = DecimalField("Yield Strength", validators=[Optional()])
    tensile = DecimalField("Tensile Strength", validators=[Optional()])

class ElasticForm(FlaskForm):
    class Meta:
        csrf = False

    modulus = DecimalField("Elastic Modulus", validators=[Optional()])
    poisson = DecimalField("Poission\'s Ratio", validators=[Optional()])

class TensileTestForm(FlaskForm):
    title = "Tensile Test Data"
    
    test_code = FieldList(StringField("Testing Standard"), min_entries=1)

    tensile_data = FieldList(FormField(TensileForm), min_entries=1)
    elastic_data = FieldList(FormField(ElasticForm), min_entries=1)
    
    yield_units = RadioField("Pressure Units", choices=[("MPa", "MPa"), ("ksi", "ksi")], validators=[Optional()])
    tensile_units = RadioField("Pressure Units", choices=[("MPa", "MPa"), ("ksi", "ksi")], validators=[Optional()])
    modulus_units = RadioField("Elastic Modulus Units", choices=[("MPa", "MPa"), ("ksi", "ksi")], validators=[Optional()])
    
    therm_coeff = FieldList(DecimalField("Coefficient of Thermal Expansion"), min_entries=1, validators=[Optional()])
    therm_coeff_units = RadioField("Test Pressure Units", choices=[("umc", "μm/m °C"), ("uif", "μin/in °F")], validators=[Optional()])
    # TODO: stress-strain curve
    

class CharpyDataForm(FlaskForm):
    class Meta:
        csrf = False
    charpy = DecimalField("Charpy Energy", validators=[DataRequired()])
    shear_area = DecimalField("Shear Area (%)", validators=[Optional()])
    temperature = DecimalField("Test Temperature", validators=[Optional()])
    
class CharpyTestForm(FlaskForm):
    class Meta:
        csrf = False
    size = SelectField("Specimen Size", choices=[("full","Full"), ("half", "Half")], validators=[DataRequired()])
    location = SelectField("Test Location", choices=[("WM", "WM"), ("HAZ", "HAZ"), ("BM", "BM"), ("FL", "FL"), ("FL2", "FL+2mm"), ("FL5", "FL+5mm")], validators=[DataRequired()])
    charpy_data = FieldList(FormField(CharpyDataForm), min_entries=1)
    charpy_units = RadioField("Charpy Energy Units", choices=[("J", "J"), ("ftlbs", "ft-lbs")], validators=[DataRequired()])
    temp_units = RadioField("Temperature Units", choices=[("C", "°C"), ("F", "°F")], validators=[Optional()])
    
class MultiCharpyTestsForm(FlaskForm):
    class Meta:
        csrf = False
    title = "Charpy Test Data"
    test_code = FieldList(StringField("Testing Standard"), min_entries=1)
    charpy_tests = FieldList(FormField(CharpyTestForm), min_entries=1)
    
class TestDataForm(FlaskForm):
    title = "Test Data"
    tensile_tests = FormField(TensileTestForm)

    go_cancel = SubmitField("Back")
    go_done = SubmitField("Next")
