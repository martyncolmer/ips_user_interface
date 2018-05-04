
from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms import StringField
from wtforms import SelectField, SubmitField
from wtforms.validators import InputRequired, NumberRange


class SearchActivityForm(FlaskForm):
    search_activity = StringField(label='Search activity')
    search_button = SubmitField(label='Search')
    advanced_search = SubmitField(label='Advanced search')
    run_type_list = [('-1', 'All Runs'),
                     ('0', 'Live'),
                     ('1', 'Published'),
                     ('2', 'Test'),
                     ('3', 'Deleted')]
    run_type_filter = SelectField(label='RunType', choices=run_type_list)


class CreateRunForm(FlaskForm):
    run_name = StringField(label='Name',
                           validators=[InputRequired()])
    run_description = StringField(label='Description',
                                  validators=[InputRequired()])


class DateSelectionForm(FlaskForm):
    months = [('00', 'Select Month'),
              ('01', 'January'), ('02', 'February'), ('03', 'March'), ('04', 'April'),
              ('05', 'May'), ('06', 'June'), ('07', 'July'), ('08', 'August'),
              ('09', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')]
    import datetime
    now = datetime.datetime.now()

    s_day = IntegerField(label='Day', validators=[InputRequired(), NumberRange(min=1, max=31)])
    s_month = SelectField(label='Month', choices=months, validators=[InputRequired()])
    s_year = IntegerField(label='Year', validators=[InputRequired(), NumberRange(min=1991, max=now.year + 1)])

    e_day = IntegerField(label='Day', validators=[InputRequired(), NumberRange(min=1, max=31)])
    e_month = SelectField(label='Month', choices=months)
    e_year = IntegerField(label='Year', validators=[InputRequired(), NumberRange(min=1991, max=now.year + 1)])
