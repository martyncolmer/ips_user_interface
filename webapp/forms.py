
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
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
    months = [('', 'Select Month'),
              ('01', 'January'), ('02', 'February'), ('03', 'March'), ('04', 'April'),
              ('05', 'May'), ('06', 'June'), ('07', 'July'), ('08', 'August'),
              ('09', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')]
    import datetime
    now = datetime.datetime.now()

    s_day = IntegerField(label='Day', validators=[InputRequired(), NumberRange(min=1, max=31)])
    s_month = SelectField(label='Month', choices=months, validators=[InputRequired()])
    s_year = IntegerField(label='Year', validators=[InputRequired(), NumberRange(min=1991, max=now.year + 1)])

    e_day = IntegerField(label='Day', validators=[InputRequired(), NumberRange(min=1, max=31)])
    e_month = SelectField(label='Month', choices=months,validators=[InputRequired()])
    e_year = IntegerField(label='Year', validators=[InputRequired(), NumberRange(min=1991, max=now.year + 2)])


class DataSelectionForm(FlaskForm):
    data_list = [('', 'Select Data'),
                 ('SHIFT_DATA|Shift Data|0', 'Shift Data'), ('TRAFFIC_DATA|Traffic Data|0', 'Traffic Data'), ('NON_RESPONSE_DATA|Non response data|0', 'Non response data'),
                 ('TRAFFIC_DATA|Tunnel data|3', 'Tunnel data'), ('TRAFFIC_DATA|Air data|2', 'Air data'), ('TRAFFIC_DATA|Sea data|1', 'Sea data'),
                 ('UNSAMPLED_OOH_DATA|Unsampled data|0', 'Unsampled data'),
                 ('PS_SHIFT_DATA|Shift weight summary|0', 'Shift weight summary'), ('PS_NON_RESPONSE|Non response weight summary|0', 'Non response weight summary'),
                 ('PS_MINIMUMS|Minimums weight summary|0', 'Minimums weight summary'), ('PS_TRAFFIC|Sampled traffic weight summary|0', 'Sampled traffic weight summary'),
                 ('PS_UNSAMPLED_OOH|Unsampled traffic weight summary|0', 'Unsampled traffic weight summary|0'), ('PS_IMBALANCE|Imbalance weight summary|0', 'Imbalance weight summary'),
                 ('PS_FINAL|Final weight summary|0', 'Final weight summary')]

    display_data = SubmitField(label='Display data')
    data_selection = SelectField(label='Select Data', choices=data_list,validators=[InputRequired()])



class LoadDataForm(FlaskForm):

    survey_file = FileField(validators=[FileRequired(), FileAllowed(['csv'], 'File must be a .csv file.')])
    shift_file = FileField(validators=[FileRequired(), FileAllowed(['csv'], 'File must be a .csv file.')])
    non_response_file = FileField(validators=[FileRequired(), FileAllowed(['csv'], 'File must be a .csv file.')])
    unsampled_file = FileField(validators=[FileRequired(), FileAllowed(['csv'], 'File must be a .csv file.')])
    tunnel_file = FileField(validators=[FileRequired(), FileAllowed(['csv'], 'File must be a .csv file.')])
    sea_file = FileField(validators=[FileRequired(), FileAllowed(['csv'], 'File must be a .csv file.')])
    air_file = FileField(validators=[FileRequired(), FileAllowed(['csv'], 'File must be a .csv file.')])


