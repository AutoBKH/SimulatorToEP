import json
from pathlib import Path

"""
Configuration JSON
{
    "read_from": "//freenas/output",
    "write_to": "http://localhost:5000/",
    "backup_dir": "./tmp/swap/",
    "read_freq_sec": 5,
    "pass_ratio_percentage": 100,
    "corrupt_message": false,
    "read_order_swap": false,
    "duplicate_message": true
}
"""


class Configure:
    __instance = None
    _data_configuration = []
    _is_running = True
    _new_configuration_read = False

    @staticmethod
    def get_instance():
        if Configure.__instance is None:
            Configure()
        return Configure.__instance

    def __init__(self):
        if Configure.__instance is not None:
            raise Exception("This class is a singleton")
        else:
            Configure.__instance = self

        with open(Path('Simulator/config.json')) as json_data_file:
            Configure._data_configuration = json.load(json_data_file)

        Configure._is_running = True

    @staticmethod
    def get_configuration():
        return Configure._data_configuration

    @staticmethod
    def set_configuration(new_configuration):
        Configure._data_configuration = new_configuration
        Configure._new_configuration_read = False

    @staticmethod
    def get_running_status():
        return Configure._is_running

    @staticmethod
    def set_running_status(is_running):
        Configure._is_running = is_running

    @staticmethod
    def set_new_configuration_read():
        Configure._new_configuration_read = True
