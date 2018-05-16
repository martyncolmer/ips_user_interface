
from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms import StringField
from wtforms import SelectField, SubmitField
from wtforms import TextField
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


class DataSelectionForm(FlaskForm):
    data_list = [('00', 'Select Data'),
                 ('SHIFT_DATA', 'Shift Data'), ('TRAFFIC_DATA', 'Traffic Data'), ('NON_RESPONSE_DATA', 'Non response data'),
                 ('TRAFFIC_DATA', 'Tunnel data'), ('TRAFFIC_DATA', 'Air data'), ('TRAFFIC_DATA', 'Sea data'),
                 ('UNSAMPLED_OOH_DATA', 'Unsampled data'),
                 ('PS_SHIFT_DATA', 'Shift weight summary'), ('PS_NON_RESPONSE', 'Non response weight summary'),
                 ('PS_MINIMUMS', 'Minimums weight summary'), ('PS_TRAFFIC', 'Sampled traffic weight summary'),
                 ('PS_UNSAMPLED_OOH', 'Unsampled traffic weight summary'), ('PS_IMBALANCE', 'Imbalance weight summary'),
                 ('PS_FINAL', 'Final weight summary')]

    display_data = SubmitField(label='Display data')
    data_selection = SelectField(label='Select Data', choices=data_list)


class ExportSelectionForm(FlaskForm):
    """Elinor Thorne"""
    data_list = [('00', 'Select Data'),
                 ("SURVEY_SUBSAMPLE", "Survey Subsample"),
                 ("PS_FINAL", "Final Weight Summary"),
                 ("PS_SHIFT_DATA", "Shift"),
                 ("PS_NON_RESPONSE", "Non-Response"),
                 ("PS_SHIFT_DATA", "Shift Weight Summary"),
                 ("NON_RESPONSE_DATA", "Non Response Weight Summary"),
                 ("PS_MINIMUMS", "Minimum Weight Summary"),
                 ("PS_TRAFFIC", "Traffic Weight Summary"),
                 ("PS_UNSAMPLED_OOH", "Unsampled Traffic Weight Summary"),
                 ("PS_IMBALANCE", "Imbalance Weight Summary"),
                 ("ALL_DATA", "All Data"),
                 ("SAS_AIR_MILES", "Air Miles"),
                 ("ALCOHOL", "Alcohol"),
                 ("REGIONAL", "Regional"),
                 ("CONTACT", "Contact"),
                 ("MIGRATION", "Migration")]

    filename = TextField('Save as')
    display_data = SubmitField(label='Export Data')
    data_selection = SelectField(label='Select Data', choices=data_list)


