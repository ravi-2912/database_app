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


class ParamForm(Form):
    def __init__(self, parameter_text="none", units=["a","b"], *args, **kwargs):
        super(FlaskForm, self).__init__(parameter_text, units, *args, **kwargs)
        self.param = DecimalField(parameter_text)
        self.unit = RadioField('Units', choices=[(units[0], units[0]), (units[1], units[1])])
            

class PipelineForm(FlaskForm):
    title = 'Pipeline Information'
    pipe_name = StringField('Pipeline Name', validators=[DataRequired()])
    line_name = StringField('Line Name', validators=[DataRequired()])
    
    od = FieldList(FormField(ParamForm), 'outer diameter', min_entries=2)
       

    wt = DecimalField('Wall Thickness')
    wt_unit = RadioField('Units', choices=[('mm','mm'),('in','in')])
    
    dp = DecimalField('Design Pressure')
    dp_unit = RadioField('Units', choices=[('bar','bar'),('psi','psi')])
    
    mop = DecimalField('Maximum Operating Pressures')
    mop_unit = RadioField('Units', choices=[('bar','bar'),('psi','psi')])

    next = SubmitField('Next')
    prev = SubmitField('Previous')
    reset = SubmitField('Reset')