import os
import csv
import uuid
from flask import Flask, render_template, session, request, url_for, redirect, abort
from werkzeug.utils import secure_filename
from webapp import app_methods

from webapp.forms import CreateRunForm, DateSelectionForm, SearchActivityForm, DataSelectionForm, LoadDataForm, ManageRunForm
import requests
import pandas as pd

APP_DIR = os.path.dirname(__file__)
app = Flask(__name__)
app.secret_key = 'D1GG2I5C00L'


@app.route('/')
def index():
    return redirect(url_for('dashboard'), code=302)


@app.route('/login')
def login():
    return render_template('/projects/legacy/login.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
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

        # If the search button is selected filter the results on the run status and the searched word.
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


@app.route('/system_info')
def system_info():
    print(request.method)
    records = app_methods.get_system_info()
    header = records[0]
    records = records[1:]

    return render_template('/projects/legacy/john/social/system_info.html',
                           header=header,
                           records=records)


@app.route('/new_run_1', methods=['GET', 'POST'])
@app.route('/new_run_1/<run_id>', methods=['GET', 'POST'])
def new_run_1(run_id=None):
    print(request.method)
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

                return redirect('/new_run_2/'+run_id, code=302)
            else:
                # Generate new run id and store name and description to be used in run creation
                unique_id = uuid.uuid4()
                session['id'] = str(unique_id)
                return redirect('/new_run_2', code=302)
    else:
        if run_id:
            run = app_methods.get_run(run_id)
            form.run_name.default = run['name']
            form.run_description.default = run['desc']
            pass

    return render_template('/projects/legacy/john/social/new_run_1.html',
                           form=form,
                           run_id=run_id)


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            print(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))


@app.route('/new_run_2', methods=['GET', 'POST'])
@app.route('/new_run_2/<run_id>', methods=['GET', 'POST'])
def new_run_2(run_id=None):
    form = DateSelectionForm()

    print(request.values)

    # if request is a post
    if request.method == 'POST':
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

                    return redirect('/new_run_3/' + run_id, code=302)
                    pass
                else:
                    app_methods.create_run(session['id'], session['run_name'], session['run_description'],
                                           session['start_date'], session['end_date'])

                    return redirect(url_for('new_run_3'), code=302)
        else:
            flash_errors(form)
    last_entry = {}

    if 's_day' in session:
        last_entry['s_day'] = session['s_day']
        last_entry['s_month'] = session['s_month']
        last_entry['s_year'] = session['s_year']
        last_entry['e_day'] = session['e_day']
        last_entry['e_month'] = session['e_month']
        last_entry['e_year'] = session['e_year']
        print("Found session s_day")
    else:
        last_entry['s_day'] = ""
        last_entry['s_month'] = ""
        last_entry['s_year'] = ""
        last_entry['e_day'] = ""
        last_entry['e_month'] = ""
        last_entry['e_year'] = ""
        print("FOUND NOTHING")

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
@app.route('/new_run_3', methods=['GET', 'POST'])
@app.route('/new_run_3/<run_id>', methods=['GET', 'POST'])
def new_run_3(run_id=None):
    form = LoadDataForm()

    error = False

    print(request.values)
    print(request.form)

    if form.validate_on_submit():
        # Functionality has been written. Stubbed for now as we are unsure yet as to the location and method
        # of storing the csv's in a file system. Until we can access DAP and know where to store, this will remain.
        # The below code shows the method for retrieving the filename and data from the uploaded files.
        if run_id:
            # if a run_id is present in html call, run steps to replace existing files (if any)
            pass
        else:
            # if no run_id present in html call, run steps to add files to run (in whatever way this will be done)
            pass

        survey_data = form.survey_file.data
        survey_filename = form.survey_file.name
        return redirect(url_for('new_run_4'))
    elif request.method == 'GET':
        pass
    else:
        error = True

    return render_template('/projects/legacy/john/social/new_run_3.html', form=form, error=error)


@app.route('/new_run_4')
def new_run_4():
    return render_template('/projects/legacy/john/social/new_run_4.html')


@app.route('/new_run_5')
def new_run_5():
    return render_template('/projects/legacy/john/social/new_run_5.html')


@app.route('/new_run_6')
def new_run_6():
    return render_template('/projects/legacy/john/social/new_run_6.html')


@app.route('/new_run_7')
def new_run_7():
    return render_template('/projects/legacy/john/social/new_run_7.html')


@app.route('/new_run_8', methods=['GET', 'POST'])
def new_run_8():
    return render_template('/projects/legacy/john/social/new_run_8.html')


@app.route('/new_run_9')
def new_run_9():
    return render_template('/projects/legacy/john/social/new_run_9.html')


@app.route('/new_run_end')
def new_run_end():
    return render_template('/projects/legacy/john/social/new_run_end.html')


@app.route('/reference/<run_id>', methods=['GET', 'POST'])
def reference(run_id):

    form = ManageRunForm();

    status_values = {'0': 'Ready', '1': 'Completed', '2': 'Failed'}
    run_types = {'0': 'Test', '1': 'Live', '2': 'Deleted'}
    run_statuses = {'0': 'Ready', '1': 'In Progress', '2': 'Completed', '3': 'Failed'}

    run = app_methods.get_run(run_id)

    if not run:
        abort(404)

    session['id'] = run['id']
    session['run_name'] = run['name']
    session['run_description'] = run['desc']
    session['start_date'] = run['start_date']
    session['end_date'] = run['end_date']
    current_run = run

    current_run['start_date'] = current_run['start_date'][:2] + "-" + current_run['start_date'][2:4] + "-" + current_run['start_date'][4:]
    current_run['end_date'] = current_run['end_date'][:2] + "-" + current_run['end_date'][2:4] + "-" + current_run['end_date'][4:]
    current_run['status'] = run_statuses[current_run['status']]
    current_run['type'] = run_types[current_run['type']]

    form.validate()
    flash_errors(form=form)
    # If this is a post then validate if needed
    if request.method == 'POST' and form.validate():
            print(request.form)
            # If the run button is selected run the calculation steps
            if 'run_button' in request.form:
                pass
            elif 'display_button' in request.form:
                return redirect('/weights/' + current_run['id'], code=302)
            elif 'edit_button' in request.form:
                return redirect('/new_run_1/' + current_run['id'], code=302)
            elif 'export_button' in request.form:
                return redirect('/export_data/' + current_run['id'], code=302)
            elif 'manage_run_button' in request.form:
                return redirect('/reference/' + current_run['id'], code=302)

    run_status = app_methods.get_run_steps(run['id'])

    for step in run_status:
        step['STATUS'] = status_values[step['STATUS']]

    return render_template('/projects/legacy/john/social/reference.html',
                           form=form,
                           current_run=current_run,
                           run_status=run_status)


@app.route('/weights/<run_id>', methods=['GET', 'POST'])
def weights(run_id=None):
    form = DataSelectionForm()

    run = app_methods.get_run(run_id)
    if(run):
        session['id'] = run['id']
        session['run_name'] = run['name']
        session['run_description'] = run['desc']
        session['start_date'] = run['start_date']
        session['end_date'] = run['end_date']
        current_run = run

        if request.method == 'POST':
            if form.validate():
                #print(request.values)
                table_name, table_title, data_source = request.values['data_selection'].split('|')
                session['dw_table'] = table_name
                session['dw_title'] = table_title
                session['dw_source'] = data_source
                return redirect(url_for('weights_2', table=table_name, id=run['id'], source=data_source, table_title=table_title), code=302)
            else:
                flash_errors(form)
        return render_template('/projects/legacy/john/social/weights.html',
                               form=form,
                               current_run=current_run)
    else:
        abort(404)


@app.route('/weights_2/<id>', methods=['GET','POST'])
@app.route('/weights_2/<id>/<table>/<table_title>/<source>', methods=['GET','POST'])
def weights_2(id, table=None, table_title=None, source=None):

    print(request)

    if id:
        if table:
            dataframe = app_methods.get_display_data_json(table, id, source)

            return render_template('/projects/legacy/john/social/weights_2.html',
                                   table_title=table_title,
                                   table=dataframe,
                                   run_id=id)
        else:
            return redirect(url_for('weights', run_id=id), code=302)
    else:
        abort(404)


@app.route('/export_data/<run_id>')
def export_data(run_id):
    form = DataSelectionForm() # change to export form once you make one

    run = app_methods.get_run(run_id)

    session['id'] = run['id']
    session['run_name'] = run['name']
    session['run_description'] = run['desc']
    session['start_date'] = run['start_date']
    session['end_date'] = run['end_date']
    current_run = run

    return render_template('/projects/legacy/john/social/export_data.html',
                           form=form,
                           current_run=current_run)


if __name__ == '__main__':
    app.run(debug=True)
