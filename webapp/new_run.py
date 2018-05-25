from flask import request, render_template, Blueprint, session, redirect, url_for
from .forms import CreateRunForm
import uuid

bp = Blueprint('new_run', __name__, url_prefix='/new_run', static_folder='static')


@bp.route('_1', methods=['GET', 'POST'])
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
