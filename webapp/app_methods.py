import csv
import requests
import json
import pyodbc
import os
import glob
import shutil
import json
import zipfile
import pandas as pd
from io import BytesIO
from io import StringIO
import sys
from pprint import pprint


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
    # print("Username: {}".format(username))
    # print("Password: {}".format(password))
    # print("Database: {}".format(database))
    # print("Server: {}".format(server))

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


def export_csv(table_name, run_id):
    """
    Author: Elinor Thorne
    Purpose: Exports table from database to CSV in temporary location

    :return: NA
    """
    conn = get_connection()
    cur = conn.cursor()

    sql = """
    SELECT * FROM [dbo].[{}]
    WHERE [RUN_ID] = '{}'
    """.format(table_name, run_id)

    path = os.getcwd()
    filename = r"\temp\{}.csv".format(table_name)
    # print(filename)

    cur.execute(sql)

    with open(path + filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([i[0] for i in cur.description])
        writer.writerows(cur.fetchall())

    # print("CSV Created")


def insert_clob(table_name, run_id, target_filename):
    """
    Author: Elinor Thorne
    Purpose: Extracts data from temporary CSV and inserts to table as CLOB

    :return: NA
    """

    # Retrieve and convert file to CLOB
    path = os.getcwd()
    file = r"\temp\{}.csv".format(table_name)
    dir = path + file
    with open(dir, 'r') as f:
        data = f.read()

    # Create and execute SQL query
    sql = """
    INSERT INTO EXPORT_DATA_DOWNLOAD
    VALUES('{}', '{}', '{}', '{}')
    """.format(run_id, data, target_filename, table_name)

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(sql)
    except Exception as err:
        print(err)


def cleanse_temp_folder():
    """
    Author: Elinor Thorne
    Purpose: Removes temporary files from location

    :return: NA
    """

    path = r"..\webapp\temp"

    fileList = os.listdir(path)
    for fileName in fileList:
        os.remove(path + "/" + fileName)

    # for files in path:
    #     os.remove(files)
    #
    # with os.scandir(path) as entries:
    #     for entry in entries:
    #         if entry.is_file() or entry.is_symlink():
    #             os.remove(entry.path)
    #         elif entry.is_dir():
    #             shutil.rmtree(entry.path)
    #             cleanse_temp_folder()
    #         pass


def export_clob(filename):
    """
    Author: Elinor Thorne
    Purpose: Exports CLOB from database to CSV

    :return: NA
    """

    sql = """
    SELECT DOWNLOADABLE_DATA
    FROM EXPORT_DATA_DOWNLOAD
    WHERE SOURCE_TABLE = '{}'
    """.format(filename)


    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
    except Exception as err:
        print(err)
    else:
        # Retrieve string from SQL and cleanse
        data = str((data[0]))
        data = data.replace(" ", "").replace("(", "").replace(")", "").replace("'", "").replace("'", "").replace(
            "\\n", " ")

        # Convert string to list and remove last empty item
        output = data.split(" ")
        output.pop()

        # Export list to csv
        path = os.getcwd()
        filename = r"\temp\{}.csv".format(filename)
        # TODO: Change file location
        with open(path+filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            for item in output:
                # Create row of data from each item in list and commit to CSV
                row = item.split(",")
                writer.writerow(row)


def get_export_data_table(run_id):
    # Connection variables
    conn = get_connection()
    cur = conn.cursor()

    # SQL query and execute
    sql = """
    SELECT [ED_NAME]
      ,[SOURCE_TABLE]
    FROM [EXPORT_DATA_DOWNLOAD]
    WHERE ED_ID = '{}'
    """.format(run_id)
    cur.execute(sql)

    # Extract row headers - NO LONGER REQUIRED
    # row_headers = [x[0] for x in cur.description]

    # Extract rows
    rows = cur.fetchall()

    data = []
    for row in rows:
        row = str(row)
        row = row.replace("(", "").replace("'", "").replace(")", "")
        data.append(row)

    return data


if __name__ == "__main__":
    # table_name = "COLUMN_LOOKUP"
    # bad_run_id = "9e5c1872-3f8e-4ae5-85dc-c67a602d011e"
    # good_run_id = "9c67a602d011e"
    # new_run_id = "40c7fbcc-c0d8-4fee-898e-9eeacf99cb66"

    get_export_data_table('f144ec22-921f-43ff-a93c-189695336580')
