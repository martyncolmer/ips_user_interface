import os
import csv
import requests
import json
import pandas


def create_run(unique_id, run_name, run_description, start_date, end_date, run_type='0', run_status='0'):
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
    new_run['type'] = run_type
    new_run['status'] = run_status
    requests.post("http://ips-db.apps.cf1.ons.statistics.gov.uk/runs", json=new_run)

    create_run_steps(new_run['id'])


def edit_run(run_id, run_name, run_description, start_date, end_date, run_type='0', run_status='0'):
    """
    Purpose: Modifies an already existing run through a PUT request.

    :return: NA
    """

    response = requests.get("http://ips-db.apps.cf1.ons.statistics.gov.uk/runs")

    file = json.loads(response.content)
    run = file[0]

    run['name'] = run_name
    run['desc'] = run_description
    run['start_date'] = start_date
    run['end_date'] = end_date
    run['type'] = run_type
    run['status'] = run_status
    requests.put("http://ips-db.apps.cf1.ons.statistics.gov.uk/runs/"+run_id, json=run)


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

    response = requests.get("http://ips-db.apps.cf1.ons.statistics.gov.uk/runs")
    return json.loads(response.content)


def get_run(run_id):

    response = requests.get("http://ips-db.apps.cf1.ons.statistics.gov.uk/runs")
    runs = json.loads(response.content)

    for x in runs:
        if x['id'] == run_id:
            return x


def get_process_variables(run_id):

    response = requests.get('http://ips-db.apps.cf1.ons.statistics.gov.uk/process_variables/' + run_id)

    return json.loads(response.content)


def create_process_variables_set(run_id, name, user, start_date, end_date):

    response = requests.get('http://ips-db.apps.cf1.ons.statistics.gov.uk/pv_sets')
    file = json.loads(response.content)
    new_pv_set = file[0]

    new_pv_set['RUN_ID'] = run_id
    new_pv_set['NAME'] = name
    new_pv_set['USER'] = user
    new_pv_set['START_DATE'] = start_date
    new_pv_set['END_DATE'] = end_date

    requests.post('http://ips-db.apps.cf1.ons.statistics.gov.uk/pv_sets', json=new_pv_set)


def create_process_variables(run_id, json):
    response = requests.post('http://ips-db.apps.cf1.ons.statistics.gov.uk/process_variables/' + run_id, json=json)
    print(response)


def get_process_variable_sets():

    response = requests.get('http://ips-db.apps.cf1.ons.statistics.gov.uk/pv_sets')
    return json.loads(response.content)


def get_display_data(table_name, source, run_id):

    column_sets = {'SHIFT_DATA': ['PORTROUTE', 'WEEKDAY', 'ARRIVEDEPART', 'AM_PM_NIGHT', 'TOTAL'],
                   'TRAFFIC_DATA': ['PORTROUTE', 'PERIODSTART', 'PERIODEND', 'ARRIVEDEPART', 'AM_PM_NIGHT', 'TRAFFICTOTAL', 'HAUL'],
                   'NON_RESPONSE_DATA': ['PORTROUTE', 'WEEKDAY', 'ARRIVEDEPART', 'AM_PM_NIGHT', 'SAMPINTERVAL', 'MIGTOTAL', 'ORDTOTAL'],
                   'UNSAMPLED_OOH_DATA': ['PORTROUTE', 'REGION', 'ARRIVEDEPART', 'UNSAMP_TOTAL'],
                   'PS_SHIFT_DATA': ['SHIFT_PORT_GRP_PV', 'ARRIVEDEPART', 'WEEKDAY_END_PV', 'AM_PM_NIGHT_PV', 'MIGSI',
                                     'POSS_SHIFT_CROSS', 'SAMP_SHIFT_CROSS', 'MIN_SH_WT', 'MEAN_SH_WT', 'MAX_SH_WT',
                                     'COUNT_RESPS', 'SUM_SH_WT'],
                   'PS_NON_RESPONSE': ['NR_PORT_GRP_PV', 'ARRIVEDEPART', 'WEEKDAY_END_PV', 'MEAN_RESPS_SH_WT', 'COUNT_RESPS',
                                       'PRIOR_SUM', 'GROSS_RESP', 'GNR', 'MEAN_NR_WT'],
                   'PS_MINIMUMS': ['MINS_PORT_GRP_PV', 'ARRIVEDEPART', 'MINS_CTRY_GRP_PV', 'MINS_NAT_GRP_PV', 'MINS_NAT_GRP_PV',
                                   'MINS_CTRY_PORT_GRP_PV', 'MINS_CASES', 'FULLS_CASES', 'PRIOR_GROSS_MINS', 'PRIOR_GROSS_FULLS',
                                   'PRIOR_GROSS_ALL', 'MINS_WT', 'POST_SUM', 'CASES_CARRIED_FWD'],
                   'PS_TRAFFIC': ['SAMP_PORT_GRP_PV', 'ARRIVEDEPART', 'FOOT_OR_VEHICLE_PV', 'CASES', 'TRAFFICTOTAL',
                                  'SUM_TRAFFIC_WT', 'TRAFFIC_WT'],
                   'PS_UNSAMPLED_OOH': ['UNSAMP_PORT_GRP_PV', 'ARRIVEDEPART', 'UNSAMP_REGION_GRP_PV', 'CASES', 'SUM_PRIOR_WT',
                                        'SUM_UNSAMP_TRAFFIC_WT', 'UNSAMP_TRAFFIC_WT'],
                   'PS_IMBALANCE': ['FLOW', 'SUM_PRIOR_WT', 'SUM_IMBAL_WT'],
                   'PS_FINAL': ['SERIAL', 'SHIFT_WT', 'NON_RESPONSE_WT', 'MINS_WT', 'TRAFFIC_WT',
                                'UNSAMP_TRAFFIC_WT', 'IMBAL_WT', 'FINAL_WT']
                   }

    connection = get_connection()

    columns = ','.join(column_sets[table_name])

    sql_command = "SELECT " + columns + " FROM " + table_name + " WHERE RUN_ID = '" + run_id + "'"

    if int(source) > 0:
        sql_command += " AND DATA_SOURCE_ID = " + source

    print(sql_command)
    df = pandas.read_sql(sql_command, connection)

    return df


def get_connection(credentials_file=
                          r"\\nsdata3\Social_Surveys_team\CASPA\IPS\IPSCredentials_SQLServer.json"):
    """
    Author     : thorne1
    Date       : May 2018
    Purpose    : Function to connect to database and return connection object
    Returns    : Connection (Object)
    Params     : credentials_file is set to default location unless user points elsewhere
    """
    pass
    # Get credentials and decrypt
    # user = ss.get_keyvalue_from_json("User", credentials_file)
    # password = ss.get_keyvalue_from_json("Password", credentials_file)
    # database = ss.get_keyvalue_from_json('Database', credentials_file)
    # server = ss.get_keyvalue_from_json('Server', credentials_file)


    # Commented out due to no longer using pyodbc.
    # Attempt to connect to the database
    # try:
    #     conn = pyodbc.connect(driver="{SQL Server}", server=server, database=database, uid=user, pwd=password,
    #                           autocommit=True)
    # except Exception as err:
    #     print(err)
    #     return False
    # else:
    #     return conn


def get_display_data_json(table_name, run_id=None, data_source=None):
    column_sets = {'SHIFT_DATA': ['PORTROUTE', 'WEEKDAY', 'ARRIVEDEPART', 'AM_PM_NIGHT', 'TOTAL'],
                   'TRAFFIC_DATA': ['PORTROUTE', 'PERIODSTART', 'PERIODEND', 'ARRIVEDEPART', 'AM_PM_NIGHT', 'TRAFFICTOTAL', 'HAUL'],
                   'NON_RESPONSE_DATA': ['PORTROUTE', 'WEEKDAY', 'ARRIVEDEPART', 'AM_PM_NIGHT', 'SAMPINTERVAL', 'MIGTOTAL', 'ORDTOTAL'],
                   'UNSAMPLED_OOH_DATA': ['PORTROUTE', 'REGION', 'ARRIVEDEPART', 'UNSAMP_TOTAL'],
                   'PS_SHIFT_DATA': ['SHIFT_PORT_GRP_PV', 'ARRIVEDEPART', 'WEEKDAY_END_PV', 'AM_PM_NIGHT_PV', 'MIGSI',
                                     'POSS_SHIFT_CROSS', 'SAMP_SHIFT_CROSS', 'MIN_SH_WT', 'MEAN_SH_WT', 'MAX_SH_WT',
                                     'COUNT_RESPS', 'SUM_SH_WT'],
                   'PS_NON_RESPONSE': ['NR_PORT_GRP_PV', 'ARRIVEDEPART', 'WEEKDAY_END_PV', 'MEAN_RESPS_SH_WT', 'COUNT_RESPS',
                                       'PRIOR_SUM', 'GROSS_RESP', 'GNR', 'MEAN_NR_WT'],
                   'PS_MINIMUMS': ['MINS_PORT_GRP_PV', 'ARRIVEDEPART', 'MINS_CTRY_GRP_PV', 'MINS_NAT_GRP_PV', 'MINS_NAT_GRP_PV',
                                   'MINS_CTRY_PORT_GRP_PV', 'MINS_CASES', 'FULLS_CASES', 'PRIOR_GROSS_MINS', 'PRIOR_GROSS_FULLS',
                                   'PRIOR_GROSS_ALL', 'MINS_WT', 'POST_SUM', 'CASES_CARRIED_FWD'],
                   'PS_TRAFFIC': ['SAMP_PORT_GRP_PV', 'ARRIVEDEPART', 'FOOT_OR_VEHICLE_PV', 'CASES', 'TRAFFICTOTAL',
                                  'SUM_TRAFFIC_WT', 'TRAFFIC_WT'],
                   'PS_UNSAMPLED_OOH': ['UNSAMP_PORT_GRP_PV', 'ARRIVEDEPART', 'UNSAMP_REGION_GRP_PV', 'CASES', 'SUM_PRIOR_WT',
                                        'SUM_UNSAMP_TRAFFIC_WT', 'UNSAMP_TRAFFIC_WT'],
                   'PS_IMBALANCE': ['FLOW', 'SUM_PRIOR_WT', 'SUM_IMBAL_WT'],
                   'PS_FINAL': ['SERIAL', 'SHIFT_WT', 'NON_RESPONSE_WT', 'MINS_WT', 'TRAFFIC_WT',
                                'UNSAMP_TRAFFIC_WT', 'IMBAL_WT', 'FINAL_WT']
                   }

    address = "http://ips-db.apps.cf1.ons.statistics.gov.uk/" + table_name
    if run_id:
        address = address + "/" + run_id

    if data_source:
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


def create_run_steps(run_id):
    """
    Purpose: Creates a new set of run steps for a newly generated run.

    :return: NA
    """
    route = "http://ips-db.apps.cf1.ons.statistics.gov.uk/run_steps/" + run_id

    requests.post(route)


def get_run_steps(run_id):
    address = "http://ips-db.apps.cf1.ons.statistics.gov.uk/run_steps/" + run_id

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
    route = "http://ips-db.apps.cf1.ons.statistics.gov.uk/run_steps/"+run_id+"/"+value

    if step_number:
        route = route + "/" + step_number

    requests.put(route)


def edit_process_variables(run_id, json_dictionary):
    """
    :param run_id:
    :param pv_content:
    :param pv_name:
    :param reason_for_change:
    :return:
    """
    response = requests.delete("http://ips-db.apps.cf1.ons.statistics.gov.uk/process_variables/" + run_id)

    create_process_variables(run_id, json_dictionary)


def get_all_run_ids():

    response = requests.get('http://ips-db.apps.cf1.ons.statistics.gov.uk/pv_sets')
    dictionary_of_pv_sets = json.loads(response.content)

    list_of_run_ids = []

    for record in dictionary_of_pv_sets:
        list_of_run_ids.append(record['RUN_ID'])

    return list_of_run_ids