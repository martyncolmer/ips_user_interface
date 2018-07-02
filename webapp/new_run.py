from flask import request, render_template, Blueprint, session, redirect, url_for, jsonify
from .forms import CreateRunForm, DateSelectionForm, LoadDataForm
from . import app_methods
import uuid
import csv
import io


bp = Blueprint('new_run', __name__, url_prefix='/new_run', static_folder='static')


@bp.route('/new_run_1', methods=['GET', 'POST'])
@bp.route('/new_run_1/<run_id>', methods=['GET', 'POST'])
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

                return redirect('/new_run/new_run_2/'+run_id, code=302)
            else:
                # Generate new run id and store name and description to be used in run creation
                unique_id = uuid.uuid4()
                session['id'] = str(unique_id)
                return redirect('/new_run/new_run_2', code=302)
    else:
        if run_id:
            run = app_methods.get_run(run_id)
            form.run_name.default = run['name']
            form.run_description.default = run['desc']
            pass

    return render_template('/projects/legacy/john/social/new_run_1.html',
                           form=form,
                           run_id=run_id)


@bp.route('/new_run_2', methods=['GET', 'POST'])
@bp.route('/new_run_2/<run_id>', methods=['GET', 'POST'])
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

                    return redirect('/new_run/new_run_3/' + run_id, code=302)
                    pass
                else:
                    app_methods.create_run(session['id'], session['run_name'], session['run_description'],
                                           session['start_date'], session['end_date'])

                    return redirect('/new_run/new_run_3', code=302)

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
@bp.route('/new_run_3', methods=['GET', 'POST'])
@bp.route('/new_run_3/<run_id>', methods=['GET', 'POST'])
def new_run_3(run_id=None):
    form = LoadDataForm()

    error = False

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

        # Import survey data
        # survey_data = form.survey_file.data
        # stream = io.StringIO(survey_data.stream.read().decode("UTF8"), newline=None)
        # survey_csv = csv.DictReader(stream)
        # survey_csv.fieldnames = [name.upper() for name in survey_csv.fieldnames]
        # survey_json = list(survey_csv)
        # print(survey_json)
        # app_methods.import_data('SHIFT_DATA', session['id'], survey_json)


        #TODO: Write a function to clear down import tables (by run_id?). Returning 500 which i think is due to duplicate records being added.

        # External

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

        return redirect('/new_run/new_run_4')
    elif request.method == 'GET':
        pass
    else:
        error = True

    return render_template('/projects/legacy/john/social/new_run_3.html', form=form, error=error)


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