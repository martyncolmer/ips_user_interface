import csv
import requests
import json
import pyodbc
import os
import shutil
import zipfile
import pandas as pd
from io import BytesIO
from io import StringIO
import sys


APP_DIR = os.path.dirname(__file__)
def export_clob2(run_id):
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
        output = str((data[0]))
        output = output.replace("('", "").replace("', )", "")
        # data = output.split("), (")
        # print(data)
        print(output)
        sys.exit()


        # output = output.replace(" ", "").replace("(", "").replace(")", "").replace("'", "").replace("'", "").replace(
        #     "\\n", " ")

        # Convert string to list and remove last empty item
        data = output.split(" ")
        data.pop()

        print(data)

        # Export list to csv
        with open(r"\\nsdata3\Social_Surveys_team\CASPA\IPS\El's Temp VDI Folder\exporty.csv", "w",
                  newline="") as csvfile:
            writer = csv.writer(csvfile)
            for item in data:
                # Create row of data from each item in list and commit to CSV
                row = item.split(",")
                writer.writerow(row)

def insert_clob2(table_name, run_id):
    # Assign connection variables
    conn = get_connection()
    cur = conn.cursor()

    # Get table data
    sql = """
    SELECT * FROM [dbo].[{}]
    """.format(table_name)
    cur.execute(sql)

    # Convert data to string and insert as CLOB
    data = str(cur.fetchall())
    data = data.replace("'", '"')

    sql = """
    INSERT INTO EXPORT_DATA_DOWNLOAD
    VALUES('{}', '{}')
    """.format(run_id, data)

    cur.execute(sql)

def export_zip2(table_name, fname):
    # Create csv file from user input
    filename = "{}.csv".format(fname)
    print(filename)

    # Retrieve data to temporary dataframe
    conn = get_connection()
    cur = conn.cursor()
    sql = """
        SELECT * FROM [dbo].[{}]
        """.format(table_name)
    df = pd.read_sql(sql, conn)

    # Create the in-memory file-like object
    in_memory = BytesIO()

    # Get a handle to the in-memory zip
    zf = zipfile.ZipFile(in_memory, "a", zipfile.ZIP_DEFLATED, False)

    # Write the file to the in-memory zip
    zf.writestr(filename, df)

    in_memory.seek(0)
    data = in_memory.read()

    # with open(in_memory, 'w', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerow([i[0] for i in cur.description])
    #     writer.writerows(cur.fetchall())

    with open(r"\\nsdata3\Social_Surveys_team\CASPA\IPS\El's Temp VDI Folder\test") as out:
        out.write(data)



    # # TODO: Create temp folder in export_csv
    # # Create file and memory locations
    # # source = r"..\webapp\temp\{}.csv".format(table_name)
    # memory_file = io.BytesIO()
    #
    # # Zip it
    # zipfile.ZipFile(memory_file, mode='w').write(source, target_filename + ".csv")
    # memory_file.seek(0)
    #
    # # Remove CSV from temp folder
    # cleanse_temp_folder()
    #
    #
    #
    #
    #
    #
    # path = os.getcwd()
    # filename = r"\temp\{}.csv".format(table_name)


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
    """
    Author: Elinor Thorne
    Purpose: Exports table from database to CSV in temporary location

    :return: NA
    """
    conn = get_connection()
    cur = conn.cursor()

    sql = """
    SELECT * FROM [dbo].[{}]
    """.format(table_name)

    path = os.getcwd()
    filename = r"\temp\{}.csv".format(table_name)
    print(filename)

    cur.execute(sql)

    with open(path + filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([i[0] for i in cur.description])
        writer.writerows(cur.fetchall())

    print("CSV Created")


def insert_clob(table_name, run_id):
    """
    Author: Elinor Thorne
    Purpose: Extracts data from temporary CSV and inserts to table as CLOB

    :return: NA
    """

    # Retrieve and convert file to CLOB
    path = os.getcwd()
    # file = r"webapp/temp/PS_SHIFT_DATA.csv"
    file = r"\temp\{}.csv".format(table_name)
    dir = path + file
    # os.scandir(dir)
    print(dir)
    with open(dir, 'r') as f:
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

    print("CLOB inserted")


def cleanse_temp_folder():
    """
    Author: Elinor Thorne
    Purpose: Removes temporary files from location

    :return: NA
    """

    path = r"..\webapp\temp"

    with os.scandir(path) as entries:
        for entry in entries:
            if entry.is_file() or entry.is_symlink():
                os.remove(entry.path)
            elif entry.is_dir():
                shutil.rmtree(entry.path)
                cleanse_temp_folder()
            pass


def export_clob(run_id, filename):
    """
    Author: Elinor Thorne
    Purpose: Exports CLOB from database to CSV

    :return: NA
    """

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
        data = str((data[0]))
        data = data.replace(" ", "").replace("(", "").replace(")", "").replace("'", "").replace("'", "").replace(
            "\\n", " ")

        # Convert string to list and remove last empty item
        output = data.split(" ")
        output.pop()

        # Export list to csv
        # TODO: Change file location
        with open(r"\\nsdata3\Social_Surveys_team\CASPA\IPS\El's Temp VDI Folder\{}.csv".format(filename), "w",
                  newline="") as csvfile:
            writer = csv.writer(csvfile)
            for item in output:
                # Create row of data from each item in list and commit to CSV
                row = item.split(",")
                writer.writerow(row)

if __name__ == "__main__":
    # table_name = "COLUMN_LOOKUP"
    # bad_run_id = "9e5c1872-3f8e-4ae5-85dc-c67a602d011e"
    # good_run_id = "9c67a602d011e"
    # new_run_id = "40c7fbcc-c0d8-4fee-898e-9eeacf99cb66"
    #
    # insert_clob(new_run_id)
    # export_clob(new_run_id)

    # table_name = "COLUMN_LOOKUP"
    # insert_clob(table_name, new_run_id)
    # export_clob(new_run_id)
    # export_zip(table_name)

    # table_name = "PS_SHIFT_DATA"
    # run_id = "9e5c1872-3f8e-4ae5-85dc-c67a602d011e"
    # insert_clob(table_name, run_id)

    cleanse_temp_folder()
