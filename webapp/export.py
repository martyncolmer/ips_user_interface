import os
import io
import zipfile
from flask import request, render_template, Blueprint, session, redirect, send_file, abort
from webapp.forms import ExportSelectionForm
from webapp.app_methods import create_export_data_download
from webapp.app_methods import export_clob
from webapp.app_methods import get_export_data_table
from webapp.app_methods import delete_export_data
from webapp.app_methods import get_run

bp = Blueprint('export', __name__, url_prefix='', static_folder='static')


@bp.route('/reference_export/<run_id>', methods=['GET', 'POST'])
@bp.route('/reference_export/<run_id>/<new_export>/<msg>', methods=['GET', 'POST'])
def reference_export(run_id, new_export="0", msg="", data=""):
    run_statuses = {'0': 'Ready', '1': 'In Progress', '2': 'Completed', '3': 'Failed'}

    # Retrieve run information
    run = get_run(run_id)

    if run:
        session['id'] = run['id']
        session['run_name'] = run['name']
        session['run_description'] = run['desc']
        session['start_date'] = run['start_date']
        session['end_date'] = run['end_date']
        current_run = run

        current_run['start_date'] = current_run['start_date'][:2] + "/" + current_run['start_date'][2:4] + "/" + current_run['start_date'][4:]
        current_run['end_date'] = current_run['end_date'][:2] + "/" + current_run['end_date'][2:4] + "/" + current_run['end_date'][4:]
        current_run['status'] = run_statuses[current_run['status']]

        # Retrieve table data
        try:
            data = get_export_data_table(run_id)
        except Exception as err:
            print(err)

        # Generate New Export button
        if request.method == 'POST':
            return redirect('/export_data/' + run_id)

        return render_template('/projects/legacy/john/social/reference_export_test.html',
                               current_run=current_run,
                               data=data,
                               new_export=str(new_export),
                               msg=str(msg))
    else:
        abort(404)


@bp.route('/export_data/<run_id>/<file_name>/<source_table>', methods=['DELETE', 'GET'])
@bp.route('/export_data/<run_id>', methods=['GET', 'POST', 'DELETE'])
def export_data(run_id):
    if run_id:
        form = ExportSelectionForm()
        run = get_run(run_id)

        session['current_run_id'] = run['id']
        session['run_name'] = run['name']
        session['run_description'] = run['desc']
        session['start_date'] = run['start_date']
        session['end_date'] = run['end_date']

        current_run = run

        if request.method == 'POST' and form.validate():
            # Get values from front end
            sql_table = request.values['data_selection']
            target_filename = request.values['filename']

            # Try to insert data to clob
            if create_export_data_download(run_id, sql_table, target_filename) == False:
                return render_template('/projects/legacy/john/social/export_data.html', form=form,
                                       current_run=current_run,
                                       data="0")
            return redirect('/reference_export/' + run_id)

        elif request.method == 'POST':
            if 'cancel_button' in request.form:
                return redirect('/reference_export/' + current_run['id'], code=302)

        return render_template('/projects/legacy/john/social/export_data_test.html', form=form, current_run=current_run,
                               data="1")

    else:
        abort(404)


@bp.route('/download_data/<run_id>/<file_name>/<source_table>')
def download_data(run_id, file_name, source_table):
    if run_id:
        # Assign variables
        memory_file = io.BytesIO()

        # Export source table as clob
        export_clob(run_id, file_name, source_table)

        # Zip file (# source = file to be zipped. file_name = zip name)
        zipfile.ZipFile(memory_file, mode='w').write(file_name + ".csv")
        memory_file.seek(0)
        os.remove(file_name + ".csv")

        return send_file(memory_file, attachment_filename='{}.zip'.format(file_name))

    else:
        abort(404)
