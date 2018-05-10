import os
import csv
from webapp import app_methods


def test_get_system_info():
    """
    Purpose: Tests the get_system_info method's functionality.
    """
    res = app_methods.get_system_info();

    # Need a test to check system info is pulling correctly
    # (should these tests be done when the data is not hard coded?)
    assert True


def test_create_run():
    """
    Purpose: Tests the create_run method's functionality.
    """
    pass
    # f = open(os.path.join(APP_DIR, '../webapp/resources/run_list.csv'), encoding='utf-8')
    # reader = csv.reader(f)
    # records_before = list(reader)
    # number_of_runs_before = len(records_before)
    # f.close()
    #
    # res = app_methods.create_run('Test-ID-000','TestRun','Run created by automated test','10051991','08052018','0','6')
    #
    # f = open(os.path.join(APP_DIR, '../webapp/resources/run_list.csv'), encoding='utf-8')
    # reader = csv.reader(f)
    # records_after = list(reader)
    # number_of_runs_after = len(records_after)
    # f.close()
    #
    # assert number_of_runs_after == number_of_runs_before + 1


def test_get_runs_json():
    result = app_methods.get_runs_json()
    assert isinstance(result, list)
    assert len(result) > 0


def test_get_runs_csv():
    result = app_methods.get_runs_json()
    assert isinstance(result, list)
    assert len(result) > 0