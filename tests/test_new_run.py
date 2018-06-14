import pytest
from webapp.forms import LoadDataForm
from werkzeug.datastructures import FileStorage
import webapp as web

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


class TestNewRun3:
    # Test that the standard page renders correctly.
    def test_default_page_new_run_3_renders_correctly_with_expected_text_from_get_request(self, client):
        res = client.get('/new_run/new_run_3')
        assert res.status_code == 200
        assert b'File type accepted is .csv' in res.data

    # Test that no error messages display when first seeing the basic page.
    def test_no_error_messages_on_default_page_from_get_request(self,client):
        res = client.get('/new_run/new_run_3')
        assert b'This field is required.' not in res.data
        assert b'All fields must be filled with .csv files only.' not in res.data

    # TODO: ensure that the test gives the expected number of these error messages
    # Test that an error is displayed if no files are given.
    def test_missing_files_error(self, client):
        res = client.post('/new_run/new_run_3')
        assert res.status_code == 200
        assert b'This field is required.' in res.data

    # Test that the new_run_4 page is rendered correctly when all fields are filled with csv files
    def test_progress_correctly_to_new_run_4_page_when_all_file_fields_are_filled_correctly_with_csv_files(self, client):
        # Given
        with app.test_request_context():
            dummy_file = FileStorage(filename='flanders.csv')
            form = LoadDataForm(survey_file=dummy_file,
                                shift_file=dummy_file,
                                non_response_file=dummy_file,
                                unsampled_file=dummy_file,
                                tunnel_file=dummy_file,
                                sea_file=dummy_file,
                                air_file=dummy_file)

            res = client.post('/new_run/new_run_3', data=form.data, follow_redirects=True)

        assert res.status_code == 200
        assert b'Select process variables' in res.data

    # Test that the appropriate error message is displayed if files are given but of the wrong format (not csv)
    def test_for_wrong_file_type_uploaded_error(self, client):
        # Given
        with app.test_request_context():
            dummy_file = FileStorage(filename='flanders.txt')
            new_form = LoadDataForm(survey_file=dummy_file,
                                shift_file=dummy_file,
                                non_response_file=dummy_file,
                                unsampled_file=dummy_file,
                                tunnel_file=dummy_file,
                                sea_file=dummy_file,
                                air_file=dummy_file)

            res = client.post('/new_run/new_run_3', data=new_form.data, follow_redirects=True)

        assert res.status_code == 200
        assert b'File must be a .csv file.' in res.data
