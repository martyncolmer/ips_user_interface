import os
import csv
import uuid
from flask import Flask, render_template, session, current_app, request, url_for, redirect, flash
from werkzeug.utils import secure_filename
from webapp import app_methods
from webapp.forms import CreateRunForm, DateSelectionForm, LoadDataForm


APP_DIR = os.path.dirname(__file__)
app = Flask(__name__)
app.secret_key = 'D1GG2I5C00L'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('/projects/legacy/login.html')


@app.route('/dashboard')
def dashboard():
    return render_template('/projects/legacy/john/social/dashboard.html')


@app.route('/system_info')
def system_info():
    records = app_methods.get_system_info()
    header = records[0]
    records = records[1:]

    return render_template('/projects/legacy/john/social/system_info.html',
                           header=header,
                           records=records)


@app.route('/new_run_1', methods=['GET', 'POST'])
def new_run_1():
    form = CreateRunForm()

    print(request.method)
    # if request is a post
    if request.method == 'POST' and form.validate():
        print('a')
        if request.form['submit'] == 'create_run':
            print('b')
            unique_id = uuid.uuid4()
            session['current_run_id'] = unique_id
            session['run_name'] = request.form['run_name']
            session['run_description'] = request.form['run_description']
            print('c')
            return redirect(url_for('new_run_2'), code=302)

        print('d')
    print('e')
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


@app.route('/new_run_3', methods = ['GET', 'POST'])
def new_run_3():
    form = LoadDataForm()

    if request.method == 'POST':
        if(form.validate()==False):
            flash_errors(form)
        else:
            survey_data = form.survey_file.data
            survey_filename = secure_filename(survey_data.filename)
            survey_data.save(survey_filename)

            shift_data = form.shift_file.data
            shift_filename = secure_filename(shift_data.filename)
            shift_data.save(shift_filename)

            non_response_data = form.non_response_file.data
            non_response_filename = secure_filename(non_response_data.filename)
            non_response_data.save(non_response_filename)

            unsampled_data = form.unsampled_file.data
            unsampled_filename = secure_filename(unsampled_data.filename)
            unsampled_data.save(unsampled_filename)

            tunnel_data = form.tunnel_file.data
            tunnel_filename = secure_filename(tunnel_data.filename)
            tunnel_data.save(tunnel_filename)

            sea_data = form.sea_file.data
            sea_filename = secure_filename(sea_data.filename)
            sea_data.save(sea_filename)

            air_data = form.air_file.data
            air_filename = secure_filename(air_data.filename)
            air_data.save(air_filename)

            return redirect(url_for('new_run_4'))

    return render_template('/projects/legacy/john/social/new_run_3.html', form = form)


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
