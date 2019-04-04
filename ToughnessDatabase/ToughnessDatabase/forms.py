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

    
class LinePipeForm(FlaskForm):
    class Meta:
        csrf = False

    diameter = StringField("Diameter", validators=[DataRequired()])
    thickness = StringField("Thickness", validators=[DataRequired()])
    grade = SelectField("Grade", choices=[("B", "Gr.B"), ("X42", "X42"), ("X52", "X52")], validators=[DataRequired()])
    seam_weld_type = SelectField("Weld Type", choices=[("DSAW", "DSAW"), ("EFW", "EFW"), ("ERW", "ERW"), ("SMLS", "SMLS")], validators=[DataRequired()])
    psl_no = SelectField("PSL No.", choices=[("PSL1", "1"), ("PSL2", "2")], validators=[DataRequired()])
    manufacturer = StringField("Manufacturer", validators=[Optional()])
    year_constructed = StringField("Construction Year", validators=[Optional()])
        
class PipelineForm(FlaskForm):
    title = "Pipeline Information"
    
    line_pipes = FieldList(FormField(LinePipeForm), min_entries=2)


    diameter_units = RadioField("Diameter Units", choices=[("mm", "mm"), ("inch", "inch")], validators=[Optional()])
    thickness_units = RadioField("Thickness Units", choices=[("mm", "mm"), ("inch", "inch")], validators=[Optional()])
    length = DecimalField("Pipeline Length", validators=[Optional()])
    length_units = RadioField("Length Units", choices=[("m", "m"), ("ft", "ft")], validators=[Optional()])
    
    
    
    
    design_code = FieldList(StringField("Design Code"), min_entries=1)
    design_press = FieldList(DecimalField("Design Pressure"), validators=[Optional()], min_entries=1, label="Design Pressure")
    design_press_units = RadioField("Pressure Units", choices=[("bar", "bar"), ("psi", "psi")], validators=[Optional()])
    design_temp = FieldList(DecimalField("Design Temperatures"), validators=[Optional()], min_entries=1, label="Design Temperature")
    design_temp_units = RadioField("Temperature Units", choices=[("C", "°C"), ("F", "°F")], validators=[Optional()])
    design_life = DecimalField("Design Life in Years", validators=[Optional()])
    year_commissioned = DecimalField("Commissioning Year", validators=[Optional()])

    oper_press = FieldList(DecimalField("Operating Pressure"), validators=[Optional()], min_entries=1, label="Operating Pressure")
    oper_press_units = RadioField("Pressure Units", choices=[("bar", "bar"), ("psi", "psi")], validators=[Optional()])
    oper_temp = FieldList(DecimalField("Operating Temperatures"), validators=[Optional()], min_entries=1, label="Operating Temperature")
    oper_temp_units = RadioField("Temperature Units", choices=[("C", "°C"), ("F", "°F")], validators=[Optional()])

    test_press = FieldList(DecimalField("Test Pressure"), validators=[Optional()], min_entries=1, label="Test Pressure")
    test_press_units = RadioField("Test Pressure Units", choices=[("bar", "bar"), ("psi", "psi")], validators=[Optional()])
    test_year = DecimalField("Test Year", validators=[Optional()])
    
    go_cancel = SubmitField("Cancel")
    go_done = SubmitField("Done")

class TensileForm(FlaskForm):
    class Meta:
        csrf = False

    yields = DecimalField("Yield Strength", validators=[Optional()])
    tensile = DecimalField("Tensile Strength", validators=[Optional()])
    modulus = DecimalField("Elastic Modulus", validators=[Optional()])
    poisson = DecimalField("Poission\'s Ratio", validators=[Optional()])
    therm_coeff = DecimalField("Coefficient of Thermal Expansion", validators=[Optional()])

  

class TensileTestForm(FlaskForm):
    title = "Tensile Test Data"
    
    test_code = FieldList(StringField("Testing Standard"), min_entries=1)

    tensile_data = FieldList(FormField(TensileForm), min_entries=1)
    
    yield_units = RadioField("Pressure Units", choices=[("MPa", "MPa"), ("ksi", "ksi")], validators=[Optional()])
    tensile_units = RadioField("Pressure Units", choices=[("MPa", "MPa"), ("ksi", "ksi")], validators=[Optional()])
    modulus_units = RadioField("Elastic Modulus Units", choices=[("MPa", "MPa"), ("ksi", "ksi")], validators=[Optional()])
    therm_coeff_units = RadioField("Test Pressure Units", choices=[("umc", "μm/m °C"), ("uif", "μin/in °F")], validators=[Optional()])
    # TODO: stress-strain curve
    

class CharpyDataForm(FlaskForm):
    class Meta:
        csrf = False
    
    size = SelectField("Specimen Size", choices=[("full","Full"), ("half", "Half")], validators=[DataRequired()])
    location = SelectField("Test Location", choices=[("WM", "WM"), ("HAZ", "HAZ"), ("BM", "BM"), ("FL", "FL"), ("FL2", "FL+2mm"), ("FL5", "FL+5mm")], validators=[DataRequired()])
    charpy = DecimalField("Charpy Energy", validators=[DataRequired()])
    shear_area = DecimalField("Shear Area (%)", validators=[Optional()])
    temperature = DecimalField("Test Temperature", validators=[Optional()])

    
class MultiCharpyTestsForm(FlaskForm):
    class Meta:
        csrf = False
    title = "Charpy Test Data"
    test_code = FieldList(StringField("Testing Standard"), min_entries=1)
    charpy_tests = FieldList(FormField(CharpyDataForm), min_entries=1)
    charpy_units = RadioField("Charpy Energy Units", choices=[("J", "J"), ("ftlbs", "ft-lbs")], validators=[DataRequired()])
    temp_units = RadioField("Temperature Units", choices=[("C", "°C"), ("F", "°F")], validators=[Optional()])
    
class TestDataForm(FlaskForm):
    title = "Test Data"
    tensile_tests = FormField(TensileTestForm)
    charpy_test_data = FormField(MultiCharpyTestsForm)

    go_cancel = SubmitField("Cancel")
    go_done = SubmitField("Done")
