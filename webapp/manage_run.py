from flask import request, render_template, Blueprint, session, redirect, url_for, abort
from .forms import ManageRunForm, DataSelectionForm
from . import app_methods

bp = Blueprint('manage_run', __name__, url_prefix='/manage_run', static_folder='static')

@bp.route('/<run_id>', methods=['GET', 'POST'])
def manage_run(run_id):

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

    # If this is a post then validate if needed
    if request.method == 'POST' and form.validate():
            print(request.form)
            # If the run button is selected run the calculation steps
            if 'run_button' in request.form:
                pass
            elif 'display_button' in request.form:
                return redirect('/manage_run/weights/' + current_run['id'], code=302)
            elif 'edit_button' in request.form:
                return redirect('/new_run/new_run_1/' + current_run['id'], code=302)
            elif 'export_button' in request.form:
                return redirect('/manage_run/export_data/' + current_run['id'], code=302)
            elif 'manage_run_button' in request.form:
                return redirect('/manage_run/' + current_run['id'], code=302)

    run_status = app_methods.get_run_steps(run['id'])

    for step in run_status:
        step['STATUS'] = status_values[step['STATUS']]

    return render_template('/projects/legacy/john/social/manage_run.html',
                           form=form,
                           current_run=current_run,
                           run_status=run_status)


@bp.route('/weights/<run_id>', methods=['GET', 'POST'])
def weights(run_id=None):
    form = DataSelectionForm()

    run = app_methods.get_run(run_id)
    if run:
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
                return redirect(url_for('manage_run.weights_2', table=table_name, id=run['id'], source=data_source, table_title=table_title), code=302)
        return render_template('/projects/legacy/john/social/weights.html',
                               form=form,
                               current_run=current_run)
    else:
        abort(404)


@bp.route('/weights_2/<id>', methods=['GET','POST'])
@bp.route('/weights_2/<id>/<table>/<table_title>/<source>', methods=['GET','POST'])
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
            return redirect(url_for('manage_run.weights', run_id=id), code=302)
    else:
        abort(404)


@bp.route('/export_data/<run_id>')
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

