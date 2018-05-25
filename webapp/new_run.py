from flask import request, render_template, Blueprint, session, redirect, url_for
from .forms import CreateRunForm, DateSelectionForm, LoadDataForm
from . import app_methods
import uuid

bp = Blueprint('new_run', __name__, url_prefix='/new_run', static_folder='static')


@bp.route('/new_run_1', methods=['GET', 'POST'])
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
            return redirect(url_for('new_run.new_run_2'), code=302)

    return render_template('/projects/legacy/john/social/new_run_1.html',
                           form=form)


@bp.route('/new_run_2', methods=['GET', 'POST'])
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

                return redirect(url_for('new_run.new_run_3'), code=302)
        else:
            pass
            #flash_errors(form)

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


@bp.route('/new_run_3', methods = ['GET', 'POST'])
def new_run_3():
    form = LoadDataForm()

    error = False

    if form.validate_on_submit():
        # Functionality has been written. Stubbed for now as we are unsure yet as to the location and method
        # of storing the csv's in a file system. Until we can access DAP and know where to store, this will remain.
        # The below code shows the method for retrieving the filename and data from the uploaded files.

        survey_data = form.survey_file.data
        survey_filename = form.survey_file.name
        return redirect(url_for('new_run.new_run_4'))
    elif request.method == 'GET':
        pass
    else:
        error = True

    return render_template('/projects/legacy/john/social/new_run_3.html', form = form, error = error)


@bp.route('/new_run_4')
def new_run_4():
    return render_template('/projects/legacy/john/social/new_run_4.html')


@bp.route('/new_run_5')
def new_run_5():
    return render_template('/projects/legacy/john/social/new_run_5.html')


@bp.route('/new_run_6')
def new_run_6():
    return render_template('/projects/legacy/john/social/new_run_6.html')


@bp.route('/new_run_7')
def new_run_7():
    return render_template('/projects/legacy/john/social/new_run_7.html')


@bp.route('/new_run_8', methods=['GET', 'POST'])
def new_run_8():
    return render_template('/projects/legacy/john/social/new_run_8.html')


@bp.route('/new_run_9')
def new_run_9():
    return render_template('/projects/legacy/john/social/new_run_9.html')


@bp.route('/new_run_end')
def new_run_end():
    return render_template('/projects/legacy/john/social/new_run_end.html')