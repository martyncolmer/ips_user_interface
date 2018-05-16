import os
import csv
import requests
import json
import subprocess
import datetime
import pyodbc
import os
import shutil
import survey_support as ss


APP_DIR = os.path.dirname(__file__)


def create_run(unique_id, run_name, run_description, start_date, end_date, run_status='0', run_type='6'):
    """
    Purpose: Creates a new run and adds it to the current list of runs (.csv currently but will be to database).

    :return: NA
    """
    response = requests.get("http://ips-db.apps.cf1.ons.statistics.gov.uk/runs")

    file = json.loads(response.content)
    new_run = file[0]

    new_run['id'] = unique_id
    new_run['name'] = run_name
    new_run['desc'] = run_description
    new_run['start_date'] = start_date
    new_run['end_date'] = end_date
    new_run['status'] = run_status
    new_run['type'] = run_type

    requests.post("http://ips-db.apps.cf1.ons.statistics.gov.uk/runs", json=new_run)

    # Commented out old csv method as json replaced, once comfortably using json this can be deleted.
    # new_entry = str(unique_id) + "," + run_name + "," + run_description + "," + start_date + "," + end_date + "," + run_status + "," + run_type + "\n"
    # f = open('../webapp/resources/run_list.csv', 'a')
    # f.write(new_entry)
    # f.close()


def get_system_info():
    """
    Purpose: Collects and returns the current build's system info to be displayed on the web application.

    :return: List of records
    """

    f = open(os.path.join(APP_DIR, '../webapp/resources/ips_system_info.csv'), encoding='utf-8')
    reader = csv.reader(f)
    records = list(reader)
    f.close()

    return records


def get_runs_json():

    requests.get("http://ips-db.apps.cf1.ons.statistics.gov.uk/runs")
    response = requests.get("http://ips-db.apps.cf1.ons.statistics.gov.uk/runs")
    return json.loads(response.content)


def get_runs_csv():
    """Read csv and return as a list of lists."""

    f = open(os.path.join(APP_DIR, '../webapp/resources/run_list.csv'), encoding='utf-8')
    reader = csv.reader(f)
    records = list(reader)

    return records


def get_run(run_id):

    response = requests.get("http://ips-db.apps.cf1.ons.statistics.gov.uk/runs")
    runs = json.loads(response.content)

    for x in runs:
        if x['id'] == run_id:
            return x


def get_connection(credentials_file=
                          r"\\nsdata3\Social_Surveys_team\CASPA\IPS\IPSCredentials_SQLServer.json"):
    """
    Author     : thorne1
    Date       : May 2018
    Purpose    : Function to connect to database and return connection object
    Returns    : Connection (Object)
    Params     : credentials_file is set to default location unless user points elsewhere
    """

    # Get credentials and decrypt
    user = ss.get_keyvalue_from_json("User", credentials_file)
    password = ss.get_keyvalue_from_json("Password", credentials_file)
    database = ss.get_keyvalue_from_json('Database', credentials_file)
    server = ss.get_keyvalue_from_json('Server', credentials_file)

    # Attempt to connect to the database
    try:
        conn = pyodbc.connect(driver="{SQL Server}", server=server, database=database, uid=user, pwd=password,
                              autocommit=True)
    except Exception as err:
        print(err)
        return False
    else:
        return conn


def export_csv(table_name):
    conn = get_connection()
    cur = conn.cursor()

    sql = """
    SELECT * FROM [dbo].[{}]
    """.format(table_name)

    path = os.getcwd()
    filename = r"\temp\{}.csv".format(table_name)

    cur.execute(sql)

    with open(path + filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([i[0] for i in cur.description])
        writer.writerows(cur.fetchall())


def cleanse_temp_foler():
    path = r"..\webapp\temp"

    with os.scandir(path) as entries:
        for entry in entries:
            if entry.is_file() or entry.is_symlink():
                os.remove(entry.path)
            elif entry.is_dir():
                shutil.rmtree(entry.path)



