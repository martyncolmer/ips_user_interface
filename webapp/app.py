import os
import csv
import uuid
from flask import Flask, render_template, session, request, url_for, redirect, abort
from werkzeug.utils import secure_filename
from webapp import app_methods

from webapp.forms import CreateRunForm, DateSelectionForm, SearchActivityForm, DataSelectionForm, LoadDataForm, ManageRunForm
import requests
import pandas as pd

# app = Flask(__name__)
#
#
#
# @app.route('/')
# def index():
#     return redirect(url_for('dashboard'), code=302)
#
#
# @app.route('/login')
# def login():
#     return render_template('/projects/legacy/login.html')
#
#
# if __name__ == '__main__':
#     app.run(debug=True)
