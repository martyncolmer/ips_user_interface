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
    runs = app_methods.get_runs()
    app_methods.create_run("AUTOMATED-TEST-RUN-ID", "AUTOMATED_TEST_NAME", "This is an **AUTOMATED** test. - DO NOT RUN", "01012018", "01012018", '2', '6')
    new_runs = app_methods.get_runs()

    # Check no new run has been created (Creation should be declined due to the primary key constraint)
    assert len(runs) == len(new_runs)


def test_get_runs():
    """
    Purpose: Tests the get_runs method's functionality.
    """
    result = app_methods.get_runs()
    assert isinstance(result, list)
    assert len(result) > 0


def test_get_display_data():
    """
    Purpose: Tests the get_display_data method's functionality.
    """
    real_table_name = 'SHIFT_DATA'
    fake_table_name = 'NO_DATA'

    df1 = app_methods.get_display_data(real_table_name)

    df2 = app_methods.get_display_data(fake_table_name)

    # Dataframe should not be empty
    assert df1.empty is False

    # Dataframe should be empty
    assert df2.empty is True
