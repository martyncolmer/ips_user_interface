from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import IntegerField
from wtforms.validators import Regexp
from wtforms import StringField
from wtforms import SelectField, SubmitField
from wtforms.validators import NoneOf
from wtforms.validators import InputRequired, NumberRange


class SearchActivityForm(FlaskForm):
    search_activity = StringField(label='Search activity')
    search_button = SubmitField(label='Search')
    advanced_search = SubmitField(label='Advanced search')
    run_type_list = [('-1', 'All Runs'),
                     ('0', 'Ready'),
                     ('1', 'In Progress'),
                     ('2', 'Completed'),
                     ('3', 'Failed')]
    run_type_filter = SelectField(label='RunType', choices=run_type_list)


class CreateRunForm(FlaskForm):
    run_name = StringField(label='Name',
                           validators=[InputRequired()])
    run_description = StringField(label='Description',
                                  validators=[InputRequired()])


class DateSelectionForm(FlaskForm):

    import datetime
    now = datetime.datetime.now()

    months = [('', 'Select Period'), ('', '---------'),
              ('Q1', 'Quarter 1'), ('Q2', 'Quarter 2'), ('Q3', 'Quarter 3'), ('Q4', 'Quarter 4'),
              ('', '---------'),
              ('01', 'January'), ('02', 'February'), ('03', 'March'), ('04', 'April'),
              ('05', 'May'), ('06', 'June'), ('07', 'July'), ('08', 'August'),
              ('09', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')]

    years = [('', 'Select Year'),('', '---------'),
             (str(now.year-10), now.year-10), (str(now.year-9), now.year-9), (str(now.year-8), now.year-8),
             (str(now.year - 7), now.year - 7), (str(now.year-6), now.year-6), (str(now.year-5), now.year-5),
             (str(now.year - 4), now.year - 4), (str(now.year-3), now.year-3), (str(now.year-2), now.year-2),
             (str(now.year - 1), now.year - 1), (str(now.year), now.year),
             ]
    s_month = SelectField(label='Month', choices=months, validators=[InputRequired()])
    s_year = SelectField(label='Year', choices=years)#, validators=[InputRequired()])


class ExportSelectionForm(FlaskForm):
    data_list = [('', ''),
                 ("SURVEY_SUBSAMPLE", "Survey Subsample"),
                 ("PS_FINAL", "Final Weight Summary"),
                 ("SHIFT_DATA", "Shift"),
                 ("NON_RESPONSE_DATA", "Non-Response"),
                 ("PS_SHIFT_DATA", "Shift Weight Summary"),
                 ("PS_NON_RESPONSE", "Non Response Weight Summary"),
                 ("PS_MINIMUMS", "Minimum Weight Summary"),
                 ("PS_TRAFFIC", "Traffic Weight Summary"),
                 ("PS_UNSAMPLED_OOH", "Unsampled Traffic Weight Summary"),
                 ("PS_IMBALANCE", "Imbalance Weight Summary")]
                 # ("ALL_DATA", "All Data"),
                 # ("SAS_AIR_MILES", "Air Miles"),
                 # ("ALCOHOL", "Alcohol"),
                 # ("REGIONAL", "Regional"),
                 # ("CONTACT", "Contact"),
                 # ("MIGRATION", "Migration")]

    filename = StringField(label='Save file as',
                           validators=[InputRequired(), Regexp(r'^[\w+-]+$'), NoneOf([" ", ".", ",", "'"])])
    data_selection = SelectField(label='Select Data', choices=data_list, validators=[InputRequired()])
    display_data = SubmitField(label='Export Data')
    cancel_button = SubmitField(label='Cancel')


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
    data_selection = SelectField(label='Select Data', choices=data_list, validators=[InputRequired()])


class LoadDataForm(FlaskForm):

    survey_file = FileField(validators=[FileRequired(), FileAllowed(['csv'], 'File must be a .csv file.')])
    shift_file = FileField(validators=[FileRequired(), FileAllowed(['csv'], 'File must be a .csv file.')])
    non_response_file = FileField(validators=[FileRequired(), FileAllowed(['csv'], 'File must be a .csv file.')])
    unsampled_file = FileField(validators=[FileRequired(), FileAllowed(['csv'], 'File must be a .csv file.')])
    tunnel_file = FileField(validators=[FileRequired(), FileAllowed(['csv'], 'File must be a .csv file.')])
    sea_file = FileField(validators=[FileRequired(), FileAllowed(['csv'], 'File must be a .csv file.')])
    air_file = FileField(validators=[FileRequired(), FileAllowed(['csv'], 'File must be a .csv file.')])


class ManageRunForm(FlaskForm):
    run_button = SubmitField(label='Run Selected')
    edit_button = SubmitField(label='Edit Run')
    display_button = SubmitField(label='Display Weights')
    export_button = SubmitField(label='Export')
    manage_run_button = SubmitField(label='Manage Run')
