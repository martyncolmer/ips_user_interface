import json
import os
import uuid
import io
import zipfile
from flask import Flask, render_template, session, request, url_for, redirect, send_file, abort, flash
from webapp import app_methods
from webapp.forms import CreateRunForm
from webapp.forms import DateSelectionForm
from webapp.forms import SearchActivityForm
from webapp.forms import DataSelectionForm
from webapp.forms import ExportSelectionForm
from webapp.forms import LoadDataForm
from webapp.app_methods import create_export_data_download
from webapp.app_methods import export_clob
from webapp.app_methods import get_export_data_table
from webapp.app_methods import delete_export_data
from webapp.app_methods import get_export_file

from flask import request, render_template, Blueprint, session, redirect
from . import app_methods

bp = Blueprint('export', __name__, url_prefix='', static_folder='static')


@bp.route('/reference_export/<run_id>', methods=['GET', 'POST'])
@bp.route('/reference_export/<run_id>/<new_export>/<msg>', methods=['GET', 'POST'])
def reference_export(run_id, new_export="0", msg="", data=""):
    # Retrieve run information
    run = app_methods.get_run(run_id)

    if run:

        session['current_run_id'] = run['id']
        session['run_name'] = run['name']
        session['run_description'] = run['desc']
        session['start_date'] = run['start_date']
        current_run = run

        # Retrieve table data
        try:
            data = get_export_data_table(run_id)
        except Exception as err:
            print(err)

        # Generate New Export button
        if request.method == 'POST':
            return redirect('/export_data/' + run_id)

        return render_template('/projects/legacy/john/social/reference_export.html',
                               current_run=current_run,
                               data=data,
                               new_export=str(new_export),
                               msg=str(msg))
    else:
        abort(404)


@bp.route('/export_data/<run_id>/<file_name>/<source_table>', methods=['DELETE', 'GET'])
@bp.route('/export_data/<run_id>', methods=['GET', 'POST', 'DELETE'])
def export_data(run_id, file_name=None, source_table=None):
    if run_id:
        form = ExportSelectionForm()
        run = app_methods.get_run(run_id)

        session['current_run_id'] = run['id']
        session['run_name'] = run['name']
        session['run_description'] = run['desc']
        session['start_date'] = run['start_date']
        session['end_date'] = run['end_date']

        current_run = run

        if request.method == 'GET':
            get_export_file(run_id, file_name, source_table)

        if request.method == 'DELETE':
            delete_export_data(run_id, file_name, source_table)

        if request.method == 'POST' and form.validate():
            # Get values from front end
            sql_table = request.values['data_selection']
            target_filename = request.values['filename']

            # Export table to temporary CSV and return success code
            new_export = 0
            msg = ""

            if msg == "":
                msg = "Export was stored successfully.  See below to download."

            # Insert data to clob
            create_export_data_download(run_id, sql_table, target_filename)

            return redirect('/reference_export/' + run_id + '/' + str(new_export) + '/' + msg)
        elif request.method == 'POST':
            if 'cancel_button' in request.form:
                return redirect('/reference_export/' + current_run['id'], code=302)

        return render_template('/projects/legacy/john/social/export_data.html', form=form, current_run=current_run)

    else:
        abort(404)


@bp.route('/download_data/<run_id>/<file_name>/<source_table>')
def download_data(run_id, file_name, source_table):
    if run_id:
        # Assign variables
        memory_file = io.BytesIO()

        export_clob(run_id, file_name, source_table)

        # Zip file (# source = file to be zipped. file_name = zip name)
        zipfile.ZipFile(memory_file, mode='w').write(file_name + ".csv")
        memory_file.seek(0)
        os.remove(file_name + ".csv")

        return send_file(memory_file, attachment_filename='{}.zip'.format(file_name))

    else:
        abort(404)
