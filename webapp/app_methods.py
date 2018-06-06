import csv
import requests
import pyodbc
import os
import json
import datetime


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


def export_csv(sql_table, run_id):
    """
    Author: Elinor Thorne
    Purpose: Exports table from database to CSV in temporary location

    :return: NA
    """
    # Connection variables
    conn = get_connection()
    cur = conn.cursor()

    # Create and execute SQL query
    sql = """
    SELECT * FROM [dbo].[{}]
    WHERE [RUN_ID] = '{}'
    """.format(sql_table, run_id)
    cur.execute(sql)

    # HARD-CODED file locations
    path = os.getcwd()
    filename = r"\temp\{}.csv".format(sql_table)

    # Write data to CSV
    with open(path + filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([i[0] for i in cur.description])
        writer.writerows(cur.fetchall())


def insert_clob(sql_table, run_id, target_filename):
    """
    Author: Elinor Thorne
    Purpose: Extracts data from temporary CSV and inserts to table as CLOB

    :return: NA
    """

    # Retrieve temporary CSV and convert to CLOB
    path = os.getcwd()
    file = r"\temp\{}.csv".format(sql_table)
    dir = path + file
    with open(dir, 'r') as f:
        data = f.read()

    # Create and execute SQL query
    sql = """
    INSERT INTO EXPORT_DATA_DOWNLOAD
    VALUES('{}', '{}', '{}', '{}', (SELECT GETDATE()))
    """.format(run_id, data, target_filename, sql_table)

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

    # HARD-CODED FILE LOCATION
    path = r"..\webapp\temp"

    # Iterate through file and delete every object
    fileList = os.listdir(path)
    for fileName in fileList:
        os.remove(path + "/" + fileName)


def export_clob(run_id, file_name):
    """
    Author: Elinor Thorne
    Purpose: Exports CLOB from database to CSV

    :return: NA
    """

    # Create and execute SQL query
    sql = """
    SELECT DOWNLOADABLE_DATA
    FROM EXPORT_DATA_DOWNLOAD
    WHERE ED_ID = '{}'
    AND ED_NAME = '{}'
    """.format(run_id, file_name)

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
    except Exception as err:
        print(err)
    else:
        # Retrieve string from SQL and cleanse
        print(data)
        data = str((data[0]))
        data = data.replace(" ", "").replace("(", "").replace(")", "").replace("'", "").replace("'", "").replace(
            "\\n", " ")

        # Convert string to list and remove last empty item
        output = data.split(" ")
        output.pop()

        # Export list to csv in HARD-CODED FILE LOCATION
        path = os.getcwd()
        filename = r"\temp\{}.csv".format(file_name)
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
    SELECT [FILENAME]
      ,[SOURCE_TABLE]
    FROM [EXPORT_DATA_DOWNLOAD]
    WHERE RUN_ID = '{}'
    ORDER BY [DATE_CREATED] DESC
    """.format(run_id)
    cur.execute(sql)

    # Extract rows
    rows = cur.fetchall()

    # Append rows to list
    data = []
    for row in rows:
        row = str(row)
        row = row.replace("(", "").replace("'", "").replace(")", "")
        data.append(row)

    return(data)


if __name__ == "__main__":
    # table_name = "COLUMN_LOOKUP"
    # bad_run_id = "9e5c1872-3f8e-4ae5-85dc-c67a602d011e"
    # good_run_id = "9c67a602d011e"
    # new_run_id = "40c7fbcc-c0d8-4fee-898e-9eeacf99cb66"

    get_export_data_table('9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
