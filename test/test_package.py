from pytest import fixture
from subprocess import run
from requests import post
from json import load
from time import sleep

post_address = "http://0.0.0.0:8080/"

input_file_path = "test/assets/input_data.json"

# paths to ground truth test results files
input_module_expected_output_file_path = "test/assets/input_module_expected_output.json"
processing_1_module_expected_output_file_path = "test/assets/processing_1_module_expected_output.json"
processing_2_module_expected_output_file_path = "test/assets/processing_2_module_expected_output.json"
output_module_expected_output_file_path = "test/assets/output_expected_output.json"

# paths to test results files generated by the pipeline
input_module_report_file_path = "test/artifacts/input_module_report.json"
processing_1_module_report_file_path = "test/artifacts/processing_1_module_report.json"
processing_2_module_report_file_path = "test/artifacts/processing_2_module_report.json"
output_module_report_file_path = "test/artifacts/output_module_report.json"


@fixture
def setup():
    # before test - create resource
    run(["docker-compose", "-f", "test/docker-compose.test.yml", "up", "-d", "--build"])

    # sleep is required here as there is a delay between the execution of the command and the containers actually being responsive
    sleep(3)

    # load test input data 
    with open(input_file_path, "r") as input_file:
        input_data = load(input_file)

    # send data to the input container and initialize testing
    response = post(url=post_address, json=input_data)
    
    # give pipeline time to process everything due to a lot of files I/O operations with saving test results
    sleep(3)

    assert response.status_code == 200, f"Could not send data to the input container: {response.status_code} - {response.text}"


@fixture
def teardown():
    yield
    # Any teardown code for that fixture is placed after the yield.
    run(["docker-compose", "-f", "test/docker-compose.test.yml", "down", "--rmi", "all"])
    run(["rm", "-r", "test/artifacts"])


def test_input_module(setup):
    # load expected input module report (ground truths)
    input_module_expected_output = {}
    with open(input_module_expected_output_file_path, "r") as output_file:
        input_module_expected_output = load(output_file)

    # load actual input module report
    input_module_report = {}
    with open(input_module_report_file_path, "r") as output_file:
        input_module_report = load(output_file)

    assert input_module_expected_output == input_module_report, f"Generated data did not match test ground truths.\nExpected:\n{input_module_expected_output}\nGot:\n{input_module_report}"

def test_processing_1_module():
    # load expected processing 1 module report (ground truths)
    processing_1_module_expected_output = {}
    with open(processing_1_module_expected_output_file_path, "r") as output_file:
        processing_1_module_expected_output = load(output_file)

    # load actual processing 1 module report
    processing_1_module_report = {}
    with open(processing_1_module_report_file_path, "r") as output_file:
        processing_1_module_report = load(output_file)

    assert processing_1_module_expected_output == processing_1_module_report, f"Generated data did not match test ground truths.\nExpected:\n{processing_1_module_expected_output}\nGot:\n{processing_1_module_report}"

def test_processing_2_module():
    # load expected processing 2 module report (ground truths)
    processing_2_module_expected_output = {}
    with open(processing_2_module_expected_output_file_path, "r") as output_file:
        processing_2_module_expected_output = load(output_file)

    # load actual processing 2 module report
    processing_2_module_report = {}
    with open(processing_2_module_report_file_path, "r") as output_file:
        processing_2_module_report = load(output_file)

    assert processing_2_module_expected_output == processing_2_module_report, f"Generated data did not match test ground truths.\nExpected:\n{processing_2_module_expected_output}\nGot:\n{processing_2_module_report}"

def test_output_module(teardown):
    # load expected output module report (ground truths)
    output_module_expected_output = {}
    with open(output_module_expected_output_file_path, "r") as output_file:
        output_module_expected_output = load(output_file)

    # load actual output module report
    output_module_report = {}
    with open(output_module_report_file_path, "r") as output_file:
        output_module_report = load(output_file)

    assert output_module_expected_output == output_module_report, f"Generated data did not match test ground truths.\nExpected:\n{output_module_expected_output}\nGot:\n{output_module_report}"
