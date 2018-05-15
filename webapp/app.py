import os
import csv
import uuid
from flask import Flask, render_template, session, current_app, request, url_for, redirect
from webapp import app_methods
from webapp.forms import CreateRunForm, DateSelectionForm, SearchActivityForm, DataSelectionForm
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
    #print(request.method)
    form = SearchActivityForm()

    # Get the records and separate the headers and values
    #records = app_methods.get_runs_csv()
    records = app_methods.get_runs()
    header = ['Run_ID', 'Run_Name', 'Run_Description', 'Start_Date', 'End_Date', 'Run_Status', 'Run Type']
    #header = records[0]
    #records = records[1:]

    # Setup key value pairs for displaying run information
    run_statuses = {'0': 'Live', '1': 'Published', '2': 'Test', '3': 'Deleted'}
    run_types = {'1': 'MainRun', '2': 'ShiftRun', '5': 'IPSRun', '3': 'NonRespRUN', '6': 'IPSRunFR02'}

    # Reformat values to be displayed on the UI
    for record in records:
        record['start_date'] = record['start_date'][:2] + "-" + record['start_date'][2:4] + "-" + record['start_date'][4:]
        record['end_date'] = record['end_date'][:2] + "-" + record['end_date'][2:4] + "-" + record['end_date'][4:]
        record['status'] = run_statuses[record['status']]
        record['type'] = run_types[record['type']]

    # If this is a post then validate if needed
    if request.method == 'POST' and form.validate():
        print(request.form)
        flash_errors(form)

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
                           run_statuses[filter_value].lower() == x['status'].lower()]
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
def new_run_1():
    print(request.method)
    form = CreateRunForm()
    # if request is a post
    if request.method == 'POST' and form.validate():
        if request.form['submit'] == 'create_run':
            unique_id = uuid.uuid4()
            session['id'] = str(unique_id)
            session['run_name'] = request.form['run_name']
            session['run_description'] = request.form['run_description']
            return redirect(url_for('new_run_2'), code=302)

    return render_template('/projects/legacy/john/social/new_run_1.html',
                           form=form)


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            print(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))


@app.route('/new_run_2', methods=['GET', 'POST'])
def new_run_2():
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


    return render_template('/projects/legacy/john/social/new_run_2.html',
                           form=form,
                           last_entry=last_entry)


@app.route('/new_run_3')
def new_run_3():
    return render_template('/projects/legacy/john/social/new_run_3.html')


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


@app.route('/reference/<run_id>')
def reference(run_id):

    run = app_methods.get_run(run_id)

    session['id'] = run['id']
    session['run_name'] = run['name']
    session['run_description'] = run['desc']
    session['start_date'] = run['start_date']
    session['end_date'] = run['end_date']
    current_run = run

    return render_template('/projects/legacy/john/social/reference.html',
                           current_run=current_run)


@app.route('/weights/<run_id>', methods=['GET', 'POST'])
def weights(run_id):
    form = DataSelectionForm()

    run = app_methods.get_run(run_id)

    session['id'] = run['id']
    session['run_name'] = run['name']
    session['run_description'] = run['desc']
    session['start_date'] = run['start_date']
    session['end_date'] = run['end_date']
    current_run = run

    if request.method == 'POST':
        #print(request.values)
        table_name, table_title, data_source = request.values['data_selection'].split('|')
        session['dw_table'] = table_name
        session['dw_title'] = table_title
        session['dw_source'] = data_source
        return redirect(url_for('weights_2'), code=302)

    return render_template('/projects/legacy/john/social/weights.html',
                           form=form,
                           current_run=current_run)


@app.route('/weights_2')
def weights_2():

    print(request)

    dataframe = app_methods.get_display_data(session['dw_table'], session['dw_source'], session['id'])

    table_title = session['dw_title']
    return render_template('/projects/legacy/john/social/weights_2.html',
                           table_title=table_title,
                           table=dataframe)


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
