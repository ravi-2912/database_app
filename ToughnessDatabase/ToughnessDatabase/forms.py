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
    
    od = FieldList(FormField(lambda **kwargs: ParamForm(text="Outer Diameter", units=["mm", "inch"], **kwargs)), min_entries=2)
       

    next = SubmitField('Next')
    prev = SubmitField('Previous')
    reset = SubmitField('Reset')