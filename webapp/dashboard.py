
from flask import request, render_template, Blueprint, current_app
from .forms import SearchActivityForm
from . import app_methods

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard', static_folder='static')


@bp.route('/', methods=['GET', 'POST'])
def dashboard_view():
    form = SearchActivityForm()

    # Log that dashboard view has been accessed
    current_app.logger.info('Dashboard being accessed...')

    # Get the records and separate the headers and values
    try:
        records = app_methods.get_runs()
    except Exception as error:
        current_app.logger.error(error, exc_info=True)
    header = ['Run_ID', 'Run_Name', 'Run_Description', 'Start_Date', 'End_Date', 'Type', 'Status']

    # Setup key value pairs for displaying run information
    run_types = {'0': 'Test', '1': 'Live', '2': 'Deleted', '3': 'SQL', '4': 'SQL', '5': 'SQL', '6': 'SQL'}
    run_statuses = {'0': 'Ready', '1': 'In Progress', '2': 'Completed', '3': 'Failed'}

    # Reformat values to be displayed on the UI
    for record in records:
        record['RUN_STATUS'] = run_statuses[str(int(record['RUN_STATUS']))]
        record['RUN_TYPE_ID'] = run_types[str(int(record['RUN_TYPE_ID']))]

    # If this is a post then validate if needed
    if request.method == 'POST' and form.validate():

        # If the search button is selected filter the results on the run status and the searched word.
        if 'search_button' in request.form:
            search_activity = request.form['search_activity']
            filter_value = request.form['run_type_filter']
            # If the filer is -1 then no filter to apply otherwise filter using the run_status value
            if request.form['run_type_filter'] != '-1':
                records = [x for x in records
                           if (search_activity.lower() in x['RUN_ID'].lower() or
                               search_activity.lower() in x['RUN_NAME'].lower() or
                               search_activity.lower() in x['RUN_DESC'].lower() or
                               search_activity.lower() in x['START_DATE'].lower() or
                               search_activity.lower() in x['END_DATE'].lower()) and
                           run_types[filter_value].lower() == x['RUN_TYPE_ID'].lower()]
            else:
                records = [x for x in records
                           if search_activity.lower() in x['RUN_ID'].lower() or
                           search_activity.lower() in x['RUN_NAME'].lower() or
                           search_activity.lower() in x['RUN_DESC'].lower() or
                           search_activity.lower() in x['START_DATE'].lower() or
                           search_activity.lower() in x['END_DATE'].lower()]

    current_app.logger.info('Rendering dashboard now...')
    return render_template('/projects/legacy/john/social/dashboard_test.html',
                           header=header,
                           records=records,
                           form=form)
