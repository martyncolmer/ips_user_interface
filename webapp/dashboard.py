
from flask import request, render_template, Blueprint
from .forms import SearchActivityForm
from . import app_methods

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard', static_folder='static')


@bp.route('/', methods=['GET', 'POST'])
def dashboard_view():
    form = SearchActivityForm()

    # Get the records and separate the headers and values
    records = app_methods.get_runs()
    header = ['Run_ID', 'Run_Name', 'Run_Description', 'Start_Date', 'End_Date', 'Type', 'Status']

    # Setup key value pairs for displaying run information
    run_types = {'0': 'Test', '1': 'Live', '2': 'Deleted'}
    run_statuses = {'0': 'Ready', '1': 'In Progress', '2': 'Completed', '3': 'Failed'}

    # Reformat values to be displayed on the UI
    for record in records:
        record['start_date'] = record['start_date'][:2] + "-" + record['start_date'][2:4] + "-" + record['start_date'][4:]
        record['end_date'] = record['end_date'][:2] + "-" + record['end_date'][2:4] + "-" + record['end_date'][4:]
        record['status'] = run_statuses[record['status']]
        record['type'] = run_types[record['type']]

    # If this is a post then validate if needed
    if request.method == 'POST' and form.validate():
        print(request.form)
        #flash_errors(form)

        # If the search button is selected filter hte results on the run status and the searched word.
        if 'search_button' in request.form:
            search_activity = request.form['search_activity']
            filter_value = request.form['run_type_filter']
            # If the filer is -1 then no filter to apply otherwise filter using the run_status value
            if request.form['run_type_filter'] != '-1':
                records = [x for x in records
                           if (search_activity.lower() in x['id'].lower() or
                               search_activity.lower() in x['name'].lower() or
                               search_activity.lower() in x['desc'].lower() or
                               search_activity.lower() in x['start_date'].lower() or
                               search_activity.lower() in x['end_date'].lower()) and
                           run_types[filter_value].lower() == x['type'].lower()]
            else:
                records = [x for x in records
                           if search_activity.lower() in x['id'].lower() or
                           search_activity.lower() in x['name'].lower() or
                           search_activity.lower() in x['desc'].lower() or
                           search_activity.lower() in x['start_date'].lower() or
                           search_activity.lower() in x['end_date'].lower()]

    return render_template('/projects/legacy/john/social/dashboard.html',
                           header=header,
                           records=records,
                           form=form)