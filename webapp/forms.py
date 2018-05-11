
from flask_wtf import FlaskForm
from flask_wtf.file import DataRequired, FileField, FileRequired
from wtforms import IntegerField
from wtforms import StringField
from wtforms import SelectField
from wtforms.validators import InputRequired, NumberRange


class SearchForm(FlaskForm):
    age = IntegerField(label='Search By Age',
                       validators=[InputRequired()])


class AuthorSearchForm(FlaskForm):
    author = StringField(label='Search By Author',
                         validators=[InputRequired()])


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


class LoadDataForm(FlaskForm):

    survey_file = FileField(validators=[DataRequired()])
    shift_file = FileField(validators=[DataRequired()])
    non_response_file = FileField(validators=[DataRequired()])
    unsampled_file = FileField(validators=[DataRequired()])
    tunnel_file = FileField(validators=[DataRequired()])
    sea_file = FileField(validators=[DataRequired()])
    air_file = FileField(validators=[DataRequired()])


