from flask import request, render_template, Blueprint, session, redirect, url_for, jsonify, current_app
from .forms import CreateRunForm, DateSelectionForm, LoadDataForm
from . import app_methods
import uuid
import json
import csv
import io


bp = Blueprint('new_run', __name__, url_prefix='/new_run', static_folder='static')


@bp.route('/new_run_1', methods=['GET', 'POST'])
@bp.route('/new_run_1/<run_id>', methods=['GET', 'POST'])
def new_run_1(run_id=None):

    current_app.logger.info("Accessing new_run_1...")
    form = CreateRunForm()
    # if request is a post
    if request.method == 'POST' and form.validate():
        if request.form['submit'] == 'create_run':

            session['run_name'] = request.form['run_name']
            session['run_description'] = request.form['run_description']

            if run_id:
                run = app_methods.get_run(run_id)

                run['name'] = request.form['run_name']
                run['desc'] = request.form['run_description']
                # Update run name and description
                app_methods.edit_run(run_id=run_id, run_name=run['name'], run_description=run['desc'],
                                     start_date=run['start_date'], end_date=run['end_date'], run_type=run['type'],
                                     run_status='0')

                current_app.logger.info("Updated existing run details. Redirecting to new_run_2...")
                return redirect('/new_run/new_run_2/'+run_id, code=302)
            else:
                # Generate new run id and store name and description to be used in run creation
                unique_id = uuid.uuid4()
                session['id'] = str(unique_id)
                current_app.logger.info("Generated new unique_id. Redirecting to new_run_2...")
                return redirect('/new_run/new_run_2', code=302)
    else:
        if run_id:
            run = app_methods.get_run(run_id)
            form.run_name.default = run['name']
            form.run_description.default = run['desc']
            pass

    if form.run_name.errors or form.run_description.errors:
        current_app.logger.warning("Missing valid run_id or description.")

    return render_template('/projects/legacy/john/social/new_run_1.html',
                           form=form,
                           run_id=run_id)


@bp.route('/new_run_2', methods=['GET', 'POST'])
@bp.route('/new_run_2/<run_id>', methods=['GET', 'POST'])
def new_run_2(run_id=None):
    form = DateSelectionForm()

    # if request is a post
    if request.method == 'POST':
        current_app.logger.debug("Processing post request.")
        session['s_day'] = request.form['s_day']
        session['s_month'] = request.form['s_month']
        session['s_year'] = request.form['s_year']
        session['e_day'] = request.form['e_day']
        session['e_month'] = request.form['e_month']
        session['e_year'] = request.form['e_year']

        if 'last_name' in session:
            last_name = session['last_name']

        if form.validate():
            if request.form['submit'] == 'create_run':

                start_date = request.form['s_day'] + request.form['s_month'] + request.form['s_year']
                end_date = request.form['e_day'] + request.form['e_month'] + request.form['e_year']

                session['start_date'] = start_date
                session['end_date'] = end_date

                if run_id:
                    # Update run start and end dates
                    run = app_methods.get_run(run_id)
                    run['start_date'] = start_date
                    run['end_date'] = end_date
                    app_methods.edit_run(run_id=run_id, run_name=run['name'], run_description=run['desc'], start_date=run['start_date'], end_date=run['end_date'], run_type=run['type'], run_status='0')
                    current_app.logger.info("Run edited with start and end date. Redirecting to new_run_3...")

                    return redirect('/new_run/new_run_3/' + run_id, code=302)
                else:
                    app_methods.create_run(session['id'], session['run_name'], session['run_description'],
                                           session['start_date'], session['end_date'])
                    current_app.logger.info("New run created from session variables. Redirecting to new_run_3...")

                    return redirect('/new_run/new_run_3', code=302)

    last_entry = {}

    if 's_day' in session:
        last_entry['s_day'] = session['s_day']
        last_entry['s_month'] = session['s_month']
        last_entry['s_year'] = session['s_year']
        last_entry['e_day'] = session['e_day']
        last_entry['e_month'] = session['e_month']
        last_entry['e_year'] = session['e_year']
    else:
        last_entry['s_day'] = ""
        last_entry['s_month'] = ""
        last_entry['s_year'] = ""
        last_entry['e_day'] = ""
        last_entry['e_month'] = ""
        last_entry['e_year'] = ""

    if run_id:
        run = app_methods.get_run(run_id)
        last_entry['s_day'] = run['start_date'][:2]
        last_entry['s_month'] = run['start_date'][2:4]
        last_entry['s_year'] = run['start_date'][4:8]
        last_entry['e_day'] = run['end_date'][:2]
        last_entry['e_month'] = run['end_date'][2:4]
        last_entry['e_year'] = run['end_date'][4:8]

        form.s_month.default = run['start_date'][2:4]
        form.e_month.default = run['end_date'][2:4]
        form.process()

    return render_template('/projects/legacy/john/social/new_run_2.html',
                           form=form,
                           last_entry=last_entry,
                           run_id=run_id)


# TODO: Implement edit run functionality when how we're dealing with files is determined.
@bp.route('/new_run_3', methods=['GET', 'POST'])
@bp.route('/new_run_3/<run_id>', methods=['GET', 'POST'])
def new_run_3(run_id=None):
    form = LoadDataForm()

    error = False

    if form.validate_on_submit():
        # Functionality has been written. Stubbed for now as we are unsure yet as to the location and method
        # of storing the csv's in a file system. Until we can access DAP and know where to store, this will remain.
        # The below code shows the method for retrieving the filename and data from the uploaded files.

        # Import survey data
        # survey_data = form.survey_file.data
        # stream = io.StringIO(survey_data.stream.read().decode("UTF8"), newline=None)
        # survey_csv = csv.DictReader(stream)
        # survey_csv.fieldnames = [name.upper() for name in survey_csv.fieldnames]
        # survey_json = list(survey_csv)
        # print(survey_json)
        # app_methods.import_data('SHIFT_DATA', session['id'], survey_json)

        #TODO: Duplicates causing issues with imports (Returning 500)... need to look into dealing with this. @TM

        # External
        current_app.logger.debug("Clearing down table records...")
        # Clear down table records associated with the current run id
        app_methods.delete_data('SHIFT_DATA', session['id'])
        app_methods.delete_data('NON_RESPONSE_DATA', session['id'])
        app_methods.delete_data('UNSAMPLED_OOH_DATA', session['id'])
        app_methods.delete_data('TRAFFIC_DATA', session['id'])

        current_app.logger.debug("Finished clearing down table records.")

        current_app.logger.info("Importing data...")

        # Import shift data
        shift_data = form.shift_file.data
        app_methods.survey_data_import('SHIFT_DATA', session['id'], shift_data)

        # Import non_response data
        non_response_data = form.non_response_file.data
        app_methods.survey_data_import('NON_RESPONSE_DATA', session['id'], non_response_data)

        # Import unsampled data
        unsampled_data = form.unsampled_file.data
        app_methods.survey_data_import('UNSAMPLED_OOH_DATA', session['id'], unsampled_data)

        # Import tunnel data
        tunnel_data = form.tunnel_file.data
        app_methods.survey_data_import('TRAFFIC_DATA', session['id'], tunnel_data)

        # Import sea data
        sea_data = form.sea_file.data
        app_methods.survey_data_import('TRAFFIC_DATA', session['id'], sea_data)

        # Import air data
        air_data = form.air_file.data
        app_methods.survey_data_import('TRAFFIC_DATA', session['id'], air_data)

        if run_id:
            current_app.logger.debug("Run_id given...")
            return redirect('/new_run/new_run_4/' + run_id, code=302)
        else:
            current_app.logger.debug("No run_id given...")
            return redirect('/new_run/new_run_4', code=302)

    elif request.method == 'GET':
        current_app.logger.info("Fulfilling GET request...")
        return render_template('/projects/legacy/john/social/new_run_3.html',
                               form=form,
                               error=error,
                               run_id=run_id)
    else:
        error = True
        current_app.logger.warning('User did not fill all fields with .csv files.')

    return render_template('/projects/legacy/john/social/new_run_3.html', form=form, error=error)


@bp.route('/new_run_4', methods=['GET', 'POST'])
def new_run_4():

    if request.method == "POST":

        session['template_id'] = request.form['selected']

        current_app.logger.info("Redirecting to new_run_5 with template_id " + session['template_id'] + "...")

        return redirect('/new_run/new_run_5')

    records = app_methods.get_process_variable_sets()

    header = ['RUN_ID', 'NAME', 'USER', 'START_DATE', 'END_DATE']

    current_app.logger.debug("Got process variable sets, rendering new_run_4.")

    return render_template('/projects/legacy/john/social/new_run_4.html', table=records, header=header)


@bp.route('/edit')
def edit(row=None):

    return render_template('/projects/legacy/john/social/edit.html', row=row)


@bp.route('/new_run_5', methods=['GET', 'POST'])
def new_run_5():

    if request.method == 'POST':

        current_app.logger.info("Getting data from Javascript modal...")

        # Method splits a the array into groups of 3
        def split_list(l, n):
            # For item i in a range that is a length of l,
            for i in range(0, len(l), n):
                # Create an index range for l of n items:
                yield l[i:i + n]

        # String coming from JavaScript
        data = request.form['pv_data']

        data = data[:-1]

        # Split the string by delimiter ^
        data_list = data.split("^")

        # Split the list into groups of 3, change 3 to whatever number you need to group by
        data_array = list(split_list(data_list, 3))

        # Array will hold the dictionaries
        data_dictionary_array = []

        # Iterate over list of lists and create a dictionary for each
        # Append each dictionary to an array
        for array in data_array:
            data = {'PV_NAME': array[0],
                    'PV_REASON': array[1],
                    'PV_CONTENT': array[2],
                    }
            data_dictionary_array.append(data)

        user = 'test_user_placeholder'

        current_app.logger.info("Getting session values...")
        current_app.logger.debug("Session values: %s, %s, %s, %s, %s, %s.", session['id'], session['run_name'],
                                 session['start_date'], session['end_date'], user)

        # Get required values from the session
        run_id = session['id']
        run_name = session['run_name']
        start_date = session['start_date']
        end_date = session['end_date']

        # Creates a new pv set if run_id doesn't already exist, otherwise delete existing rows and repopulate
        if run_id not in app_methods.get_all_run_ids():
            current_app.logger.info("New run_id given, creating new process variable set...")
            # Creates a new set of process variables, then fill the empty set with the edited javascript data
            app_methods.create_process_variables_set(run_id, run_name, user, start_date, end_date)
            # Fill newly created pv set with new process variables (for new runs)
            app_methods.create_process_variables(run_id, data_dictionary_array)
            current_app.logger.info("New process variable set created.")
        else:
            current_app.logger.info("Existing run_id given, updating records...")
            # Edit existing process variables (for edit run)
            app_methods.edit_process_variables(run_id, data_dictionary_array)
            current_app.logger.info("Records updated successfully.")

        return redirect('/manage_run/' + run_id)

    template_id = session['template_id']

    header = ['PV_NAME', 'PV_REASON', 'PV_CONTENT']

    records = app_methods.get_process_variables(template_id)

    return render_template('/projects/legacy/john/social/new_run_5.html', table=records, header=header)
