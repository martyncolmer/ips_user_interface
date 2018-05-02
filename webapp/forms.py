
from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms import StringField
from wtforms import SelectField
from wtforms import DateField
from wtforms.validators import InputRequired


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

    day = StringField(label='Day', validators=[InputRequired()])
    month = SelectField(label='Month', choices=months)
    year = StringField(label='Year', validators=[InputRequired()])

    s_day = StringField(label='Day', validators=[InputRequired()])
    s_month = SelectField(label='Month', choices=months)
    s_year = StringField(label='Year', validators=[InputRequired()])

    e_day = StringField(label='Day', validators=[InputRequired()])
    e_month = SelectField(label='Month', choices=months)
    e_year = StringField(label='Year', validators=[InputRequired()])
