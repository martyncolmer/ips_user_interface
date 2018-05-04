import os
import csv
import uuid
from flask import Flask, render_template, session, current_app, request, url_for, redirect
from webapp import app_methods
from webapp.forms import CreateRunForm, DateSelectionForm, SearchActivityForm
import requests

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
    print(request.method)
    form = SearchActivityForm()

    # Get the records and separate the headers and values
    records = app_methods.get_runs_csv()
    header = records[0]
    records = records[1:]

    # Setup key value pairs for displaying run information
    run_statuses = {'0': 'Live', '1': 'Published', '2': 'Test', '3': 'Deleted'}
    run_types = {'1': 'MainRun', '2': 'ShiftRun', '5': 'IPSRun', '3': 'NonRespRUN', '6': 'IPSRunFR02'}

    # Reformat values to be displayed on the UI
    for record in records:
        record[3] = record[3][:2] + "-" + record[3][2:4] + "-" + record[3][4:]
        record[4] = record[4][:2] + "-" + record[4][2:4] + "-" + record[4][4:]
        record[5] = run_statuses[record[5]]
        record[6] = run_types[record[6]]

    form.validate()
    flash_errors(form)

    # If this is a pose then validate if needed
    if request.method == 'POST' and form.validate():
        print(request.form)

        # If the search button is selected filter hte results on the run status and the searched word.
        if 'search_button' in request.form:
            search_activity = request.form['search_activity']
            filter_value = request.form['run_type_filter']

            # If the filer is -1 then no filter to apply otherwise filter using the run_status value
            if request.form['run_type_filter'] != '-1':
                records = [x for x in records
                           if (search_activity.lower() in x[0].lower() or
                               search_activity.lower() in x[1].lower() or
                               search_activity.lower() in x[2].lower() or
                               search_activity.lower() in x[3].lower() or
                               search_activity.lower() in x[4].lower()) and
                           run_statuses[filter_value].lower() == x[5].lower()]
            else:
                records = [x for x in records
                           if search_activity.lower() in x[0].lower() or
                           search_activity.lower() in x[1].lower() or
                           search_activity.lower() in x[2].lower() or
                           search_activity.lower() in x[3].lower() or
                           search_activity.lower() in x[4].lower()]

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
            session['current_run_id'] = unique_id
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

    # if request is a post
    if request.method == 'POST':
        if form.validate():
            if request.form['submit'] == 'create_run':
                start_date = request.form['s_day'] + request.form['s_month'] + request.form['s_year']
                end_date = request.form['e_day'] + request.form['e_month'] + request.form['e_year']

                session['start_date'] = start_date
                session['end_date'] = end_date

                app_methods.create_run(session['current_run_id'], session['run_name'], session['run_description'],
                                       session['start_date'], session['end_date'])

                return redirect(url_for('new_run_3'), code=302)
        else:
            flash_errors(form)

    return render_template('/projects/legacy/john/social/new_run_2.html',
                           form=form)


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


if __name__ == '__main__':
    app.run(debug=True)
