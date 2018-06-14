from webapp.forms import DataSelectionForm, LoadDataForm
import pytest
import webapp as web
from werkzeug.datastructures import FileStorage

app = web.create_app()

@pytest.fixture()
def client():
    """The flask test client for our app.

    This lets us trigger http requests to end points without needing a server running.
    """

    app.testing = True
    app.config["WTF_CSRF_ENABLED"] = False
    client = app.test_client()


    return client


class TestNewRun1:

    # GETS

    # No Run ID (New)
    def test_get_webpage_no_run_id_returns_ok(self, client):

        res = client.get('/new_run/new_run_1')
        assert res.status_code == 200

    def test_get_webpage_no_run_id_renders_correct_info_banner(self, client):
        res = client.get('/new_run/new_run_1')
        assert b'You are creating a new IPS run.' in res.data

    def test_get_webpage_no_run_id_renders_page_title(self, client):
        res = client.get('/new_run/new_run_1')
        assert b'Run details' in res.data

    def test_get_webpage_no_run_id_renders_step_indicator(self, client):
        res = client.get('/new_run/new_run_1')
        assert b'Step 1' in res.data

    def test_get_webpage_no_run_id_renders_run_name_label(self, client):
        res = client.get('/new_run/new_run_1')
        assert b'Name' in res.data

    def test_get_webpage_no_run_id_renders_run_description_label(self, client):
        res = client.get('/new_run/new_run_1')
        assert b'Description' in res.data

    def test_get_webpage_no_run_id_renders_save_and_continue_button(self, client):
        res = client.get('/new_run/new_run_1')
        assert b'Save and continue' in res.data

    def test_get_webpage_no_run_id_renders_cancel_button(self, client):
        res = client.get('/new_run/new_run_1')
        assert b'Cancel' in res.data

    # Valid Run ID (Edit)
    def test_get_webpage_valid_run_id_returns_ok(self, client):

        res = client.get('/new_run/new_run_1/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert res.status_code == 200

    def test_get_webpage_valid_run_id_renders_correct_info_banner(self, client):
        res = client.get('/new_run/new_run_1/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'You are editing run: 9e5c1872-3f8e-4ae5-85dc-c67a602d011e' in res.data

    def test_get_webpage_valid_run_id_renders_page_title(self, client):
        res = client.get('/new_run/new_run_1/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Run details' in res.data

    def test_get_webpage_valid_run_id_renders_step_indicator(self, client):
        res = client.get('/new_run/new_run_1/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Step 1' in res.data

    def test_get_webpage_valid_run_id_renders_run_name_label(self, client):
        res = client.get('/new_run/new_run_1/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Name' in res.data

    def test_get_webpage_valid_run_id_renders_run_description_label(self, client):
        res = client.get('/new_run/new_run_1/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Description' in res.data

    def test_get_webpage_valid_run_id_renders_save_and_continue_button(self, client):
        res = client.get('/new_run/new_run_1/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Save and continue' in res.data

    def test_get_webpage_valid_run_id_renders_cancel_button(self, client):
        res = client.get('/new_run/new_run_1/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Cancel' in res.data

    # POSTS

    # Save and continue button
    def test_pressing_save_and_continue_button_with_no_form_data_returns_ok(self, client):

        with app.test_request_context():
            # Post to page with  no form data
            res = client.post('/new_run/new_run_1')

        assert res.status_code == 200

    def test_pressing_save_and_continue_button_with_no_form_data_triggers_validation_errors(self, client):
        with app.test_request_context():
            # Post to page with no form data
            res = client.post('/new_run/new_run_1')

        # Ensure validation failed
        assert b'This field is required.' in res.data


class TestNewRun2:
    # GETS

    # No Run ID (New)
    def test_get_webpage_no_run_id_returns_ok(self, client):
        res = client.get('/new_run/new_run_2')
        assert res.status_code == 200

    def test_get_webpage_no_run_id_renders_correct_info_banner(self, client):
        res = client.get('/new_run/new_run_2')
        assert b'You are creating a new IPS run.' in res.data

    def test_get_webpage_no_run_id_renders_page_title(self, client):
        res = client.get('/new_run/new_run_2')
        assert b'Select fieldwork' in res.data

    def test_get_webpage_no_run_id_renders_step_indicator(self, client):
        res = client.get('/new_run/new_run_2')
        assert b'Step 2' in res.data

    def test_get_webpage_no_run_id_renders_start_date_label(self, client):
        res = client.get('/new_run/new_run_2')
        assert b'Start date' in res.data

    def test_get_webpage_no_run_id_renders_run_description_label(self, client):
        res = client.get('/new_run/new_run_2')
        assert b'End date' in res.data

    def test_get_webpage_no_run_id_renders_day_label(self, client):
        res = client.get('/new_run/new_run_2')
        assert b'Day' in res.data

    def test_get_webpage_no_run_id_renders_month_label(self, client):
        res = client.get('/new_run/new_run_2')
        assert b'Month' in res.data

    def test_get_webpage_no_run_id_renders_year_label(self, client):
        res = client.get('/new_run/new_run_2')
        assert b'Year' in res.data

    def test_get_webpage_no_run_id_renders_save_and_continue_button(self, client):
        res = client.get('/new_run/new_run_2')
        assert b'Save and continue' in res.data

    def test_get_webpage_no_run_id_renders_back_button(self, client):
        res = client.get('/new_run/new_run_2')
        assert b'Back' in res.data

    def test_get_webpage_no_run_id_renders_cancel_button(self, client):
        res = client.get('/new_run/new_run_2')
        assert b'Cancel' in res.data

    # Valid Run ID (Edit)
    def test_get_webpage_valid_run_id_returns_ok(self, client):
        res = client.get('/new_run/new_run_2/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert res.status_code == 200

    def test_get_webpage_valid_run_id_renders_correct_info_banner(self, client):
        res = client.get('/new_run/new_run_2/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'You are editing run: 9e5c1872-3f8e-4ae5-85dc-c67a602d011e' in res.data

    def test_get_webpage_valid_run_id_renders_page_title(self, client):
        res = client.get('/new_run/new_run_2/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Select fieldwork' in res.data

    def test_get_webpage_valid_run_id_renders_step_indicator(self, client):
        res = client.get('/new_run/new_run_2/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Step 2' in res.data

    def test_get_webpage_valid_run_id_renders_start_date_label(self, client):
        res = client.get('/new_run/new_run_2/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Start date' in res.data

    def test_get_webpage_valid_run_id_renders_run_description_label(self, client):
        res = client.get('/new_run/new_run_2/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'End date' in res.data

    def test_get_webpage_valid_run_id_renders_day_label(self, client):
        res = client.get('/new_run/new_run_2/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Day' in res.data

    def test_get_webpage_valid_run_id_renders_month_label(self, client):
        res = client.get('/new_run/new_run_2/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Month' in res.data

    def test_get_webpage_valid_run_id_renders_year_label(self, client):
        res = client.get('/new_run/new_run_2/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Year' in res.data

    def test_get_webpage_valid_run_id_renders_save_and_continue_button(self, client):
        res = client.get('/new_run/new_run_2/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Save and continue' in res.data

    def test_get_webpage_valid_run_id_renders_back_button(self, client):
        res = client.get('/new_run/new_run_2/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Back' in res.data

    def test_get_webpage_valid_run_id_renders_cancel_button(self, client):
        res = client.get('/new_run/new_run_2/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Cancel' in res.data


class TestNewRun3:
    # GETS

    # No Run ID (New)
    def test_get_webpage_no_run_id_returns_ok(self, client):
        res = client.get('/new_run/new_run_3')
        assert res.status_code == 200

    def test_get_webpage_no_run_id_renders_page_title(self, client):
        res = client.get('/new_run/new_run_3')
        assert b'Load data' in res.data

    def test_get_webpage_no_run_id_renders_step_indicator(self, client):
        res = client.get('/new_run/new_run_3')
        assert b'Step 3' in res.data

    def test_get_webpage_no_run_id_renders_survey_data_label(self, client):
        res = client.get('/new_run/new_run_3')
        assert b'Survey data' in res.data

    def test_get_webpage_no_run_id_renders_external_data_label(self, client):
        res = client.get('/new_run/new_run_3')
        assert b'External data' in res.data

    def test_get_webpage_no_run_id_renders_day_label(self, client):
        res = client.get('/new_run/new_run_3')
        assert b'Shift data' in res.data

    def test_get_webpage_no_run_id_renders_month_label(self, client):
        res = client.get('/new_run/new_run_3')
        assert b'Non_response data' in res.data

    def test_get_webpage_no_run_id_renders_year_label(self, client):
        res = client.get('/new_run/new_run_3')
        assert b'Unsampled data' in res.data

    def test_get_webpage_no_run_id_renders_day_label(self, client):
        res = client.get('/new_run/new_run_3')
        assert b'Tunnel data' in res.data

    def test_get_webpage_no_run_id_renders_month_label(self, client):
        res = client.get('/new_run/new_run_3')
        assert b'Sea data' in res.data

    def test_get_webpage_no_run_id_renders_year_label(self, client):
        res = client.get('/new_run/new_run_3')
        assert b'Air data' in res.data

    def test_get_webpage_no_run_id_renders_save_and_continue_button(self, client):
        res = client.get('/new_run/new_run_3')
        assert b'Save and continue' in res.data

    def test_get_webpage_no_run_id_renders_back_button(self, client):
        res = client.get('/new_run/new_run_3')
        assert b'Back' in res.data

    def test_get_webpage_no_run_id_renders_cancel_button(self, client):
        res = client.get('/new_run/new_run_3')
        assert b'Cancel' in res.data

    # Test that the standard page renders correctly.
    def test_get_webpage_no_run_id_renders_file_type_message(self, client):
        res = client.get('/new_run/new_run_3')
        assert b'File type accepted is .csv' in res.data

    # Test that no error messages display when first seeing the basic page.
    def test_get_webpage_no_run_id_renders_no_errors_when_first_loaded(self, client):
        res = client.get('/new_run/new_run_3')
        assert b'This field is required.' not in res.data
        assert b'All fields must be filled with .csv files only.' not in res.data


    # Valid Run ID (Edit)
    def test_get_webpage_valid_run_id_returns_ok(self, client):
        res = client.get('/new_run/new_run_3/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert res.status_code == 200

    def test_get_webpage_valid_run_id_renders_page_title(self, client):
        res = client.get('/new_run/new_run_3/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Load data' in res.data

    def test_get_webpage_valid_run_id_renders_step_indicator(self, client):
        res = client.get('/new_run/new_run_3/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Step 3' in res.data

    def test_get_webpage_valid_run_id_renders_survey_data_label(self, client):
        res = client.get('/new_run/new_run_3/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Survey data' in res.data

    def test_get_webpage_valid_run_id_renders_external_data_label(self, client):
        res = client.get('/new_run/new_run_3/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'External data' in res.data

    def test_get_webpage_valid_run_id_renders_day_label(self, client):
        res = client.get('/new_run/new_run_3/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Shift data' in res.data

    def test_get_webpage_valid_run_id_renders_month_label(self, client):
        res = client.get('/new_run/new_run_3/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Non_response data' in res.data

    def test_get_webpage_valid_run_id_renders_year_label(self, client):
        res = client.get('/new_run/new_run_3/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Unsampled data' in res.data

    def test_get_webpage_valid_run_id_renders_day_label(self, client):
        res = client.get('/new_run/new_run_3/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Tunnel data' in res.data

    def test_get_webpage_valid_run_id_renders_month_label(self, client):
        res = client.get('/new_run/new_run_3/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Sea data' in res.data

    def test_get_webpage_valid_run_id_renders_year_label(self, client):
        res = client.get('/new_run/new_run_3/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Air data' in res.data

    def test_get_webpage_valid_run_id_renders_save_and_continue_button(self, client):
        res = client.get('/new_run/new_run_3/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Save and continue' in res.data

    def test_get_webpage_valid_run_id_renders_back_button(self, client):
        res = client.get('/new_run/new_run_3/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Back' in res.data

    def test_get_webpage_valid_run_id_renders_cancel_button(self, client):
        res = client.get('/new_run/new_run_3/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Cancel' in res.data

    # Test that the standard page renders correctly.
    def test_get_webpage_valid_run_id_renders_file_type_message(self, client):
        res = client.get('/new_run/new_run_3/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'File type accepted is .csv' in res.data

    # Test that no error messages display when first seeing the basic page.
    def test_get_webpage_valid_run_id_renders_no_errors_when_first_loaded(self, client):
        res = client.get('/new_run/new_run_3/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'This field is required.' not in res.data
        assert b'All fields must be filled with .csv files only.' not in res.data

    # POSTS

    # No Run ID (New)

    # TODO: ensure that the test gives the expected number of these error messages
    # Test that an error is displayed if no files are given.
    def test_webpage_no_run_id_renders_errors_when_missing_information(self, client):
        res = client.post('/new_run/new_run_3')
        assert b'This field is required.' in res.data

    # Valid Run ID (Edit)

    # TODO: ensure that the test gives the expected number of these error messages
    # Test that an error is displayed if no files are given.
    def test_webpage_valid_run_id_renders_errors_when_missing_information(self, client):
        res = client.post('/new_run/new_run_3/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'This field is required.' in res.data
