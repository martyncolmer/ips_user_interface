import os
import csv

APP_DIR = os.path.dirname(__file__)


def create_run(unique_id,run_name, run_description, start_date, end_date):
    """
    Purpose: Creates a new run and adds it to the current list of runs (.csv currently but will be to database).

    :return: NA
    """
    
    new_entry = str(unique_id) + "," + run_name + "," + run_description + "," + start_date + "," + end_date + "," + "0" +  "," + "6" + "\n"

    f = open('../webapp/resources/run_list.csv', 'a')
    f.write(new_entry)
    f.close()


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



