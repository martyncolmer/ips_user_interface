import pandas
import csv
import requests
import os
import json
import pandas
import io
import datetime
from flask import session, render_template

APP_DIR = os.path.dirname(__file__)

API_TARGET = r'http://10.28.56.87:5000'        # This is my VDI instance IP.
#API_TARGET = r'http://localhost:5000'


def create_run(unique_id, run_name, run_description, user_id, start_date, end_date, run_type='0', run_status='0'):
    """
    Purpose: Creates a new run and adds it to the current list of runs (.csv currently but will be to database).

    :return: NA
    """
    #response = requests.get(API_TARGET + r"/runs")

    new_run = {'RUN_ID': unique_id, 'RUN_NAME': run_name, 'RUN_DESC': run_description, 'USER_ID': user_id,
               'START_DATE': start_date, 'END_DATE': end_date, 'RUN_TYPE_ID': run_type, 'RUN_STATUS': run_status}

    requests.post(API_TARGET + r"/runs", json=new_run)

    create_run_steps(new_run['RUN_ID'])


def edit_run(run_id, run_name, run_description, start_date, end_date, run_type='0', run_status='0'):
    """
    Purpose: Modifies an already existing run through a PUT request.

    :return: NA
    """

    response = requests.get(API_TARGET + r'/runs')

    file = json.loads(response.content)
    run = file[0]

    run['RUN_ID'] = run_id
    run['RUN_NAME'] = run_name
    run['RUN_DESC'] = run_description
    run['START_DATE'] = start_date
    run['END_DATE'] = end_date
    run['RUN_TYPE_ID'] = run_type
    run['RUN_STATUS'] = run_status
    requests.put(API_TARGET + r'/runs/' + run_id, json=run)


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
    """
        Purpose: Gets all of the runs to put in the list

        :return: List of JSON object runs
        """

    response = requests.get(API_TARGET+r'/runs')
    return json.loads(response.content)


def get_run(run_id):
    """
        Purpose: Gets a single run by ID

        :return: A specific JSON run object
        """
    response = requests.get(API_TARGET+r'/runs')
    runs = json.loads(response.content)

    for x in runs:
        if x['RUN_ID'] == run_id:
            return x


def get_display_data_json(table_name, run_id=None, data_source=None):
    column_sets = {'SHIFT_DATA': ['PORTROUTE', 'WEEKDAY', 'ARRIVEDEPART', 'AM_PM_NIGHT', 'TOTAL'],
                   'TRAFFIC_DATA': ['PORTROUTE', 'PERIODSTART', 'PERIODEND', 'ARRIVEDEPART', 'AM_PM_NIGHT',
                                    'TRAFFICTOTAL', 'HAUL'],
                   'NON_RESPONSE_DATA': ['PORTROUTE', 'WEEKDAY', 'ARRIVEDEPART', 'AM_PM_NIGHT', 'SAMPINTERVAL',
                                         'MIGTOTAL', 'ORDTOTAL'],
                   'UNSAMPLED_OOH_DATA': ['PORTROUTE', 'REGION', 'ARRIVEDEPART', 'UNSAMP_TOTAL'],
                   'PS_SHIFT_DATA': ['SHIFT_PORT_GRP_PV', 'ARRIVEDEPART', 'WEEKDAY_END_PV', 'AM_PM_NIGHT_PV', 'MIGSI',
                                     'POSS_SHIFT_CROSS', 'SAMP_SHIFT_CROSS', 'MIN_SH_WT', 'MEAN_SH_WT', 'MAX_SH_WT',
                                     'COUNT_RESPS', 'SUM_SH_WT'],
                   'PS_NON_RESPONSE': ['NR_PORT_GRP_PV', 'ARRIVEDEPART', 'WEEKDAY_END_PV', 'MEAN_RESPS_SH_WT',
                                       'COUNT_RESPS',
                                       'PRIOR_SUM', 'GROSS_RESP', 'GNR', 'MEAN_NR_WT'],
                   'PS_MINIMUMS': ['MINS_PORT_GRP_PV', 'ARRIVEDEPART', 'MINS_CTRY_GRP_PV', 'MINS_NAT_GRP_PV',
                                   'MINS_NAT_GRP_PV',
                                   'MINS_CTRY_PORT_GRP_PV', 'MINS_CASES', 'FULLS_CASES', 'PRIOR_GROSS_MINS',
                                   'PRIOR_GROSS_FULLS',
                                   'PRIOR_GROSS_ALL', 'MINS_WT', 'POST_SUM', 'CASES_CARRIED_FWD'],
                   'PS_TRAFFIC': ['SAMP_PORT_GRP_PV', 'ARRIVEDEPART', 'FOOT_OR_VEHICLE_PV', 'CASES', 'TRAFFICTOTAL',
                                  'SUM_TRAFFIC_WT', 'TRAFFIC_WT'],
                   'PS_UNSAMPLED_OOH': ['UNSAMP_PORT_GRP_PV', 'ARRIVEDEPART', 'UNSAMP_REGION_GRP_PV', 'CASES',
                                        'SUM_PRIOR_WT',
                                        'SUM_UNSAMP_TRAFFIC_WT', 'UNSAMP_TRAFFIC_WT'],
                   'PS_IMBALANCE': ['FLOW', 'SUM_PRIOR_WT', 'SUM_IMBAL_WT'],
                   'PS_FINAL': ['SERIAL', 'SHIFT_WT', 'NON_RESPONSE_WT', 'MINS_WT', 'TRAFFIC_WT',
                                'UNSAMP_TRAFFIC_WT', 'IMBAL_WT', 'FINAL_WT']
                   }

    address = API_TARGET + r'/' + table_name
    if run_id:
        address = address + "/" + run_id

    if data_source:

        if table_name == 'TRAFFIC_DATA':
            address = address + "/" + data_source

    response = requests.get(address)
    if response.status_code == 200:
        data = json.loads(response.content)
        df = pandas.DataFrame.from_dict(data)
        df = df[column_sets[table_name]]
    else:
        if table_name in column_sets:
            df = pandas.DataFrame(columns=column_sets[table_name])
        else:
            df = pandas.DataFrame()

    return df


def get_process_variables(run_id):

    response = requests.get(API_TARGET + r'/process_variables/' + run_id)

    return json.loads(response.content)


def create_process_variables_set(run_id, name, user, start_date, end_date):

    response = requests.get(API_TARGET + r'/pv_sets')
    file = json.loads(response.content)
    new_pv_set = file[0]

    new_pv_set['RUN_ID'] = run_id
    new_pv_set['NAME'] = name
    new_pv_set['USER'] = user
    new_pv_set['START_DATE'] = start_date
    new_pv_set['END_DATE'] = end_date

    requests.post(API_TARGET + r'/pv_sets', json=new_pv_set)


def create_process_variables(run_id, json):
    requests.post(API_TARGET + r'/process_variables/' + run_id, json=json)


def get_process_variable_sets():

    response = requests.get(API_TARGET + r'/pv_sets')
    return json.loads(response.content)


def create_run_steps(run_id):
    """
    Purpose: Creates a new set of run steps for a newly generated run.

    :return: NA
    """
    route = API_TARGET + r"/run_steps/" + run_id

    requests.post(route)


def get_run_steps(run_id):
    address = API_TARGET + r'/run_steps/' + run_id

    response = requests.get(address)

    if response.status_code == 200:
        values = json.loads(response.content)
    else:
        values = []

    return values


def edit_run_step_status(run_id, value, step_number=None):
    """
    Purpose: Modifies an already existing run's steps through a PUT request.

    :return: NA
    """
    route = API_TARGET + r'/run_steps/' + run_id + r'/' + value

    if step_number:
        route = route + "/" + step_number

    requests.put(route)


def get_export_data_table(run_id):
    """
        Purpose: Gets the export data for all the runs

        :return: List of exports as JSON
        """
    # API gateway response is a list of JSON data containing the export data for all the runs
    response = requests.get(API_TARGET + r'/EXPORT_DATA_DOWNLOAD/' + run_id)

    # Set boolean to assume records exist
    exports = 1

    # Empty data if no response
    if response.status_code == 400:
        data = [{'DATE_CREATED': '',
                 'DOWNLOADABLE_DATA': '',
                 'FILENAME': '',
                 'RUN_ID': '',
                 'SOURCE_TABLE': ''}]
        # Set boolean if no records exist
        exports = 0
        return data, exports

    # Convert response to JSON
    json_data = json.loads(response.content)

    return json_data, exports


def export_clob(run_id, target_filename, sql_table):
    """
        Purpose: Puts the export downloadable data into a text file

        :return: NA
        """
    # API gateway response to get a single export from run id, filename and the SQL table
    response = requests.get(
        API_TARGET + r'/EXPORT_DATA_DOWNLOAD' + r'/' + run_id + r'/' + target_filename + r'/' + sql_table)

    # Convert data to json
    table_data_json = json.loads(response.content)

    # Get the downloadable data
    run = table_data_json[0]['DOWNLOADABLE_DATA']

    # Put the data in a text file saved in the project root directory with prefix .csv
    with open(target_filename + ".csv", "w") as text_file:
        print(run, file=text_file)


def delete_export_data(run_id, target_filename, sql_table):
    """
            Purpose: Deletes export data

            :return: NA
            """
    # Delete the  export with run id, filename and sql table
    response = requests.delete(
        API_TARGET + r'/export_data_download/' + run_id + '/' + target_filename + '/' + sql_table)


def get_export_file(run_id, target_filename, sql_table):
    """
            Purpose: Get a single export by run id, filename and SQL table

            :return: Export as JSON
            """
    response = requests.get(
        API_TARGET + r'/EXPORT_DATA_DOWNLOAD' + r'/' + run_id + r'/' + target_filename + r'/' + sql_table)
    response = json.loads(response.content)
    return response


def create_export_data_download(run_id, sql_table, target_filename):
    """
            Purpose: Gets the export data and puts into a single long string
            :return: Boolean - posts the data to the database
            """

    # Get the export data by SQL table and run id
    try:
        response = requests.get(API_TARGET + r'/' + sql_table + r'/' + run_id)
        # Convert to JSON
        table_data_json = json.loads(response.content)
    except Exception as err:
        return False

    # TODO: THERE WILL BE A MUCH CLEANER WAY TO DO THIS

    # Lists to append data to and then combine
    columns = []
    values = []

    # Add all the columns to column list
    for x in table_data_json:
        for key in x:
            columns.append(key)
        break

    # Add all the values to a list
    for x in table_data_json:
        for key in x:
            values.append(x[key])

    # Length of columns list so we know how far to slice values
    column_length = len(columns)

    # Create string of all columns split with comma and new line
    columns_csv_data = ','.join(columns) + '\n'
    values_csv_data = ''

    # All we do here is move through values in chunks to add to the right columns
    # Slice values by column length and append to values string
    column_counter = 0
    while column_counter <= len(values):
        data_slice = values[:column_length]
        values_csv_data += ','.join(map(str, data_slice)) + '\n'
        # Delete slice so we can get the next
        del values[:column_length]
        column_counter += 1

    # Combine columns and rows to make one long csv string
    data = columns_csv_data + values_csv_data

    # Create dict with data to post
    json_data = {'DATE_CREATED': datetime.datetime.now().strftime('%Y-%d-%m %H:%M:%S'),
                 'DOWNLOADABLE_DATA': data,
                 'FILENAME': target_filename,
                 'RUN_ID': run_id,
                 'SOURCE_TABLE': sql_table}

    # Convert to json
    data = json.dumps(json_data)

    # Post data to API gateway
    requests.post(API_TARGET + r'/EXPORT_DATA_DOWNLOAD', data=data)

    return True


def edit_process_variables(run_id, json_dictionary):
    """
    :param run_id:
    :param pv_content:
    :param pv_name:
    :param reason_for_change:
    :return:
    """
    response = requests.delete(API_TARGET + r'/process_variables/' + run_id)

    create_process_variables(run_id, json_dictionary)


def get_all_run_ids():

    response = requests.get(API_TARGET + r'/pv_sets')
    dictionary_of_pv_sets = json.loads(response.content)

    list_of_run_ids = []

    for record in dictionary_of_pv_sets:
        list_of_run_ids.append(record['RUN_ID'])

    return list_of_run_ids


def import_data(table_name, run_id, json_data):

    requests.post(API_TARGET + r'/' + table_name + r'/' + run_id, json=json_data)


def delete_data(table_name, run_id=None):

    route = API_TARGET + r'/' + table_name

    if run_id:
        route = route + r'/' + run_id

    rv = requests.delete(route)
    print("DELETE - " + table_name)
    print(rv)


def survey_data_import(table_name, import_run_id, import_data_file):
    # Import  data
    stream = io.StringIO(import_data_file.stream.read().decode("ANSI"), newline=None)
    import_csv = csv.DictReader(stream)
    import_csv.fieldnames = [name.upper() for name in import_csv.fieldnames]
    print("Field Names:")
    print(import_csv.fieldnames)
    import_json = list(import_csv)
    import_data(table_name, import_run_id, import_json)


def get_run_step_requests(run_id, step_number = None):

    # Get using sql server connection
    # conn = get_sql_connection()
    # cur = conn.cursor()
    #
    # # Create and execute SQL query
    # sql = "SELECT * from [dbo].[RESPONSE] where RUN_ID = '" + run_id + "'"
    #
    # try:
    #     cur.execute(sql)
    #     result = cur.fetchall()
    # except Exception as err:
    #     # Raise (unit testing purposes) and return False to indicate table does not exist
    #     # database_logger().error(err, exc_info = True)
    #     print("An exception has been raised. IMPLEMENT LOGGING HERE")
    #     return False
    #
    # print(result)
    #
    # return result


    address = API_TARGET + r'/RESPONSE/' + run_id

    if step_number:
        address = address + r'/' + step_number

    response = requests.get(address)

    if response.status_code == 200:
        values = json.loads(response.content)
    else:
        values = []

    return values

# Added temporarily as to not write too much SQL alchemy code which will be removed from SQL when connection can be established from API Gateway
# def get_sql_connection():
#     """
#     Author       : Thomas Mahoney / Nassir Mohammad (edits)
#     Date         : 11 / 07 / 2018
#     Purpose      : Establishes a connection to the SQL Server database and returns the connection object.
#     Parameters   : in_table_name - the IPS survey records for the period.
#                    credentials_file  - file containing the server and login credentials used for connection.
#     Returns      : a pyodbc connection object.
#     Requirements : NA
#     Dependencies : NA
#     """
#
#     # Get credentials and decrypt
#     username = os.getenv("DB_USER_NAME")
#     password = os.getenv("DB_PASSWORD")
#     database = os.getenv("DB_NAME")
#     server = os.getenv("DB_SERVER")
#
#     # Attempt to connect to the database
#     try:
#         conn = pyodbc.connect(driver="{SQL Server}", server=server, database=database, uid=username, pwd=password, autocommit=True)
#     except Exception as err:
#         print("computer says no")
#         #database_logger().error(err, exc_info = True)
#         return False
#     else:
#         return conn


def create_request(run_id,step_number, json=None):
    requests.post(API_TARGET + r'/RESPONSE', json=json)


# Steps to run comes through as a string list containing the step numbers to run
def start_run(run_id, steps_to_run):
    steps_json = json.dumps(steps_to_run)
    requests.post(API_TARGET + r'/manage_run/start_run/' + str(run_id), json=steps_json)
