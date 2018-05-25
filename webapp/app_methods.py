import csv
import requests
import json
import pyodbc
import os
import shutil
import pandas as pd
import sys


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


def get_runs():

    response = requests.get("http://ips-db.apps.cf1.ons.statistics.gov.uk/runs")
    return json.loads(response.content)


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


def get_connection():
    """
    Author       : Thomas Mahoney
    Date         : 03 / 04 / 2018
    Purpose      : Establishes a connection to the SQL Server database and returns the connection object.
    Parameters   : in_table_name - the IPS survey records for the period.
                   credentials_file  - file containing the server and login credentials used for connection.
    Returns      : pyodbc connection object
    Requirements : NA
    Dependencies : NA
    """

    # Get credentials and decrypt
    username = os.getenv("DB_USER_NAME")
    password = os.getenv("DB_PASSWORD")
    database = os.getenv("DB_NAME")
    server = os.getenv("DB_SERVER")

    # My environment variables keep disappearing >:-|
    print("Username: {}".format(username))
    print("Password: {}".format(password))
    print("Database: {}".format(database))
    print("Server: {}".format(server))

    # Attempt to connect to the database
    try:
        conn = pyodbc.connect(driver="{SQL Server}", server=server, database=database, uid=username, pwd=password,
                              autocommit=True)
    except Exception as err:
        # database_logger().error(err, exc_info = True)
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


def cleanse_temp_folder():
    path = r"..\webapp\temp"

    with os.scandir(path) as entries:
        for entry in entries:
            if entry.is_file() or entry.is_symlink():
                os.remove(entry.path)
            elif entry.is_dir():
                shutil.rmtree(entry.path)


def insert_clob(run_id):
    # Retrieve and convert file to BLOB
    file = r'C:\Users\thorne1\PycharmProjects\ips_user_interface\webapp\temp\COLUMN_LOOKUP.csv'
    with open(file, 'r') as f:
        data = f.read()

    # Create and execute SQL query
    sql = """
    INSERT INTO EXPORT_DATA_DOWNLOAD
    VALUES('{}', '{}')
    """.format(run_id, data)

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(sql)
    except Exception as err:
        print(err)


def export_clob(run_id):

    sql = """
    SELECT DOWNLOADABLE_DATA
    FROM EXPORT_DATA_DOWNLOAD
    WHERE ED_ID = '{}'
    """.format(run_id)

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
    except Exception as err:
        print(err)
    else:
        # Retrieve string from SQL and cleanse
        stringy = str((data[0]))
        stringy = stringy.replace(" ", "").replace("(", "").replace(")", "").replace("'", "").replace("'", "").replace(
            "\\n", " ")

        # Convert string to list and remove last empty item
        listy = stringy.split(" ")
        listy.pop()

        # Export list to csv
        with open(r"\\nsdata3\Social_Surveys_team\CASPA\IPS\El's Temp VDI Folder\exporty.csv", "w",
                  newline="") as csvfile:
            writer = csv.writer(csvfile)
            for item in listy:
                # Create row of data from each item in list and commit to CSV
                row = item.split(",")
                writer.writerow(row)


if __name__ == "__main__":
    bad_run_id = "9e5c1872-3f8e-4ae5-85dc-c67a602d011e"
    good_run_id = "9c67a602d011e"
    # insert_clob(run_id)

    # table_name = "COLUMN_LOOKUP"
    export_clob(bad_run_id)
