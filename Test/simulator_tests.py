import pytest
import json
import threading
import time
from http import HTTPStatus
from mimesis import Development as mDevelopment
from mimesis import Path as mPath
from random import randint
from requests import post, get
from pathlib import Path
from Simulator.configure import Configure
from Simulator.dir_reader import DirReader
from Simulator.server import app
from Test import ep_simulator, spreader_file_creator

sim_url = "http://localhost:5000"
sim_ep_url = "http://localhost:5050"


@pytest.fixture(scope="session", autouse=True)
def custom_setup():
    print(f"Start from custom_setup")
    configuration = Configure()
    d = DirReader(configuration)
    d.start()
    # m1 = multiprocessing.Process(target=start_ep_simulator)
    # m1.start()
    # m2 = multiprocessing.Process(target=start_simulator)
    # m2.start()
    t1 = threading.Thread(target=start_ep_simulator)
    t1.start()
    t2 = threading.Thread(target=start_simulator)
    t2.start()
    yield print("Start of test")
    response = post(url=sim_url + "/shutdown")
    assert response.status_code == HTTPStatus.OK, print(f"response.status is {response.status_code}")
    response = post(url=sim_ep_url + "/shutdown")
    assert response.status_code == HTTPStatus.OK, print(f"response.status is {response.status_code}")
    Configure.set_running_status(False)
    # m1.kill()
    # m2.kill()
    t1.join()
    t2.join()
    print("End of test")


@pytest.fixture(scope="module", autouse=True)
def setup_test():
    yield print(f"Starting test")
    teardown_test()


def teardown_test():
    print(f"Ending test")


def get_configuration():
    data_configuration = None
    with open(Path('Simulator/config.json')) as json_data_file:
        try:
            data_configuration = json.load(json_data_file)
        except ValueError as e:
            print(f"Error while reading JSON configuration file")
        finally:
            return data_configuration


def start_ep_simulator(host='0.0.0.0', port=5050):
    ep_simulator.ep_simulator.run(debug=False, host=host, port=port)


def start_simulator(host='0.0.0.0', port=5000):
    app.run(debug=False, host=host, port=port)


def test_sanity():
    spreader_file_creator.create_dummy_ack("Test/files_from_SP", loops=2, num_files=10, interval_sec=2)
    configuration = get_configuration()
    sim_url = "http://localhost:5000"
    time.sleep(1)
    response = get(sim_url + "/config")
    data = {
        "read_from": "Test/files_from_SP",
        "write_to": "http://localhost:5050/send_event",
        "backup_dir": "Test/backup",
        "errors_dir": "Test/errors",
        "read_freq_sec": 8,
        "pass_ratio_percentage": 0,
        "number_of_duplications": 1,
        "corrupt_message": False,
        "read_order_swap": False,
        "duplicate_message": False
    }

    response = post(url=sim_url + "/config", data=data)
    response = get(sim_url + "/config")
    print(response.json())
    time.sleep(100)


@pytest.mark.parametrize('execution_number', range(11))
def test_configuration_check(execution_number):
    sim_url = "http://localhost:5000"
    p = mPath()
    d = mDevelopment()
    read_from = p.users_folder()
    backup_dir = p.users_folder()
    errors_dir = p.users_folder()
    read_freq_seq = randint(0, 9999)
    pass_ratio_percentage = randint(0, 101)
    number_of_duplications = randint(1, 11)
    corrupt_message = d.boolean()
    read_order_swap = d.boolean()
    duplicate_message = d.boolean()
    data = {
        "read_from": read_from,
        "write_to": "http://localhost:5050/send_event",
        "backup_dir": backup_dir,
        "errors_dir": errors_dir,
        "read_freq_sec": read_freq_seq,
        "pass_ratio_percentage": pass_ratio_percentage,
        "number_of_duplications": number_of_duplications,
        "corrupt_message": corrupt_message,
        "read_order_swap": read_order_swap,
        "duplicate_message": duplicate_message
    }
    response = post(url=sim_url + "/config", json=data)
    assert response.status_code == HTTPStatus.OK, print(f"response.status is {response.status_code}")
    time.sleep(1)
    response = get(sim_url + "/config")
    assert response.status_code == HTTPStatus.OK, print(f"response.status is {response.status_code}")
    assert sorted(response.json().items()) == sorted(data.items()), print(f"Configuration sent different from received")


testdata = [(spreader_file_creator.create_dummy_ack, "Test/backup2"),
            (spreader_file_creator.create_dummy_ack, "Test/backup"),
            (spreader_file_creator.create_dummy_empty, "Test/errors2"),
            (spreader_file_creator.create_dummy_empty, "Test/errors")]


@pytest.mark.parametrize("func, dir", testdata)
def test_backup_error_dir(func, dir):
    # create_dummy_ack(path, loops, num_files: int, interval_sec: int, random_selection = False):
    loops = 1
    num_files = 3
    expected_files = loops*num_files
    response = post(url=sim_url + "/stop")
    assert response.status_code == HTTPStatus.OK, print(f"response.status is {response.status_code}")
    clear_directory(dir)
    clear_directory("Test/files_from_SP")
    time.sleep(1)
    func("Test/files_from_SP", loops=loops, num_files=num_files, interval_sec=2)
    assert count_dir("Test/files_from_SP") == expected_files, print(f"Expected {expected_files} files")
    if "error" in dir:
        change_config({"errors_dir": dir})
    else:
        change_config({"backup_dir": dir})
    time.sleep(10)
    assert count_dir(dir) == expected_files, print(f"Expected {expected_files} files")


def clear_directory(dir_path):
    for file in Path(dir_path).iterdir():
        if not str(file.name).startswith(".") and file.is_file():
            file.unlink()


def count_dir(dir_path):
    count = 0
    for file in Path(dir_path).iterdir():
        if not str(file.name).startswith(".") and file.is_file():
            count += 1
    return count


def change_config(new_config: dict):
    response = post(url=sim_url + "/stop")
    assert response.status_code == HTTPStatus.OK, print(f"response.status is {response.status_code}")
    response = get(url=sim_url + "/config")
    assert response.status_code == HTTPStatus.OK, print(f"response.status is {response.status_code}")
    response_json = response.json()
    for k, v in new_config.items():
        current_conf = response_json.get(k)
        if current_conf is not None:
            response_json[k] = v
    response = post(sim_url + "/config", json=response_json)
    assert response.status_code == HTTPStatus.OK, print(f"response.status is {response.status_code}")
    response = post(url=sim_url + "/start")
    assert response.status_code == HTTPStatus.OK, print(f"response.status is {response.status_code}")

