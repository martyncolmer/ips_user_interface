import os
import csv
from flask import Flask, render_template, session, current_app, request


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
    records = get_system_info()
    header = records[0]
    records = records[1:]

    return render_template('/projects/legacy/john/social/system_info.html',
                           header=header,
                           records=records)


@app.route('/new_run_1')
def new_run_1():
    return render_template('/projects/legacy/john/social/new_run_1.html')


@app.route('/new_run_2')
def new_run_2():
    return render_template('/projects/legacy/john/social/new_run_2.html')


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


# Non decorator functions

def get_system_info():
    """Read csv and return as a list of lists."""
    f = open(os.path.join(APP_DIR, 'ips_system_info.csv'), encoding='utf-8')
    reader = csv.reader(f)
    records = list(reader)

    return records


if __name__ == '__main__':
    app.run(debug=True)
