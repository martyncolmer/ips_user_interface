import os
import csv
import requests
import json
import pandas


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

    f = open('webapp/resources/ips_system_info.csv', encoding='utf-8')
    reader = csv.reader(f)
    records = list(reader)
    f.close()

    return records


def get_runs():

    requests.get("http://ips-db.apps.cf1.ons.statistics.gov.uk/runs")
    response = requests.get("http://ips-db.apps.cf1.ons.statistics.gov.uk/runs")
    return json.loads(response.content)


def get_run(run_id):

    response = requests.get("http://ips-db.apps.cf1.ons.statistics.gov.uk/runs")
    runs = json.loads(response.content)

    for x in runs:
        if x['id'] == run_id:
            return x


def get_display_data(table_name):

    file_path = 'webapp/resources/data/' + table_name + '.csv'
    if os.path.exists(file_path):
        df = pandas.read_csv('webapp/resources/data/' + table_name + '.csv')
    else:
        df = pandas.DataFrame()

    return df
