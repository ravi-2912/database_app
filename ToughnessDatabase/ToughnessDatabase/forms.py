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
    title = 'Project Details'
    prj_name = StringField('Project Name', validators=[DataRequired()])
    prj_no = StringField('Project Number', validators=[DataRequired()])
    region_prj_no = StringField('Regional Project Number', validators=[DataRequired()])
    owner = StringField('Owner(s)')
    operator = StringField('Operator(s)')
    country = StringField('Country')
    state = StringField('State')
    city = StringField('City')
    next = SubmitField('Next')
    reset = SubmitField('Reset')


class ParamForm(FlaskForm):
    param = DecimalField("Param")
    units = RadioField("Units")
    def __init__(self, text="none", units=["a","b"], **kwargs):
        super(FlaskForm, self).__init__(**kwargs)
        self.param.label = text
        self.units.label = "{} Units".format(text)
        self.units.choices = [(units[0], units[0]), (units[1], units[1])]
        self.units.default = units[1]
        self.process()
            

class PipelineForm(FlaskForm):
    title = 'Pipeline Information'
    pipe_name = StringField('Pipeline Name', validators=[DataRequired()])
    line_name = StringField('Line Name', validators=[DataRequired()])
    line_code = StringField('Design Code')
    line_length = DecimalField('Pipeline\'s Length')
    line_length_units = RadioField('Length Units', choices=[('m', 'm'), ('ft', 'ft')])
    manu_year = DecimalField("Construction / Commissioning Year")
    od = FieldList(DecimalField('Outer Diameter'))
    od_units = RadioField('Diameter Units', choices=[('mm', 'mm'), ('inch', 'inch')])
    wt = FieldList(DecimalField('Wall Thickness'))
    wt_units = RadioField('Thickness Units', choices=[('mm', 'mm'), ('inch', 'inch')])
    grade = FieldList(SelectField('Material Grade'))
    long_seam = FieldList(SelectField('Weld Type'))
    psl_no = FieldList(SelectField('PSL'))
    pres = FieldList(DecimalField('Design / Operating Pressure'))
    press_units = RadioField('Pressure Units', choices=[('bar', 'bar'), ('psi', 'psi')])
    test_pres = FieldList(DecimalField('Test Pressure'))
    test_press_units = RadioField('Test Pressure Units', choices=[('bar', 'bar'), ('psi', 'psi')])
    temp = FieldList(DecimalField("Design / Operating Temperatures"))
    temp_units = RadioField('Temperature Units', choices=[('c', '°C'), ('f', '°F')])
    #od = FieldList(FormField(lambda **kwargs: ParamForm(text="Outer Diameter", units=["mm", "inch"], **kwargs)), min_entries=1)
    #wt = FieldList(FormField(lambda **kwargs: ParamForm(text="Wall Thickness", units=["mm", "inch"], **kwargs)), min_entries=2)
    

    next = SubmitField('Next')
    prev = SubmitField('Previous')
    reset = SubmitField('Reset')