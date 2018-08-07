from flask import request, render_template, Blueprint
from . import app_methods

bp = Blueprint('system_info', __name__, url_prefix='/system_info', static_folder='static')


@bp.route('/')
def system_info():
    print(request.method)
    records = app_methods.get_system_info()
    header = records[0]
    records = records[1:]

    return render_template('/projects/legacy/john/social/system_info_test.html',
                           header=header,
                           records=records)