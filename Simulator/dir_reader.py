import threading
import os
import json
import shutil
import uuid
import time
import random
import pickle
import jsonpickle
from requests import post
from pathlib import Path
from http import HTTPStatus
from Simulator.configure import Configure
from Simulator.event import Event

# TODO 0. See other TODOs in code
# TODO 1. Make code defensive
# TODO 2. Implement pickle packaging of message to EP


class DirReader(threading.Thread):
    def __init__(self, config):
        super().__init__()
        self._read_from = config.get_configuration().get("read_from")
        self._write_to = config.get_configuration().get("write_to")
        self._backup_dir = config.get_configuration().get("backup_dir")
        self._corrupt_message = config.get_configuration().get("corrupt_message")
        self.read_freq_sec = config.get_configuration().get("read_freq_sec")
        self._reverse_files = config.get_configuration().get("read_order_swap")
        self._duplicate_message = config.get_configuration().get("duplicate_message")
        self._pass_ratio = config.get_configuration().get("pass_ratio_percentage")
        self._guid = uuid.uuid4()
        print(f"Thread starts id {self._guid}")

    def run(self):
        url = self._write_to
        guid = uuid.uuid4()
        while Configure.get_running_status():
            time.sleep(self.read_freq_sec)
            # entries_listdir = []
            # for file in Path(self._read_from).iterdir():
            #     if file.is_file():
            #         entries_listdir.append(file)
            # entries_listdir.sort(key=os.path.getmtime, reverse=self._reverse_files)
            dir_list_ordered = self.get_dir_list_ordered()

            for file in dir_list_ordered:
                print(f"Found new file {file}. {guid}")
                if self.is_send_file():
                    f = open(str(file), "r")
                    contents = json.loads(f.read())
                    f.close()
                    time.sleep(1)
                    if self._corrupt_message:
                        contents = self.please_corrupt_message(contents)
                    contents = self.prepare_message_to_ep(contents)
                    response = post(url, data=contents)
                    if response.status_code == HTTPStatus.OK:
                        print(f"Moving file {file} to {self._backup_dir}. {guid}")
                        shutil.move(str(file), self._backup_dir)
                        print(response.json())
                    if self._duplicate_message:
                        time.sleep(1)
                        response = post(url, data=contents)
                        if response.status_code == HTTPStatus.OK:
                            print(f"Sent duplicated message")
                            print(response.json())
                else:
                    shutil.move(str(file), self._backup_dir)
                    print(f"Moving file {file} to {self._backup_dir}. {guid}")

            # entries = os.scandir(self._read_from)
            # for entry in entries:
            #     # TODO - check file endswith
            #     if entry.is_file():
            #         print(f"Found new file {entry.name}. {guid}")
            #         f = open(entry.path, "r")
            #         contents = json.loads(f.read())
            #         f.close()
            #         time.sleep(1)
            #         response = post(url, data=json.dumps(contents))
            #         if response.status_code == HTTPStatus.OK:
            #             print(f"Moving file {entry.path} to {self._backup_dir}. {guid}")
            #             shutil.move(entry.path, self._backup_dir)
            #             print(response.json())

    def is_send_file(self):
        return random.random() <= (self._pass_ratio / 100)

    def get_dir_list_ordered(self):
        dir_list_ordered = []
        for file in Path(self._read_from).iterdir():
            # TODO - should check files of specific type?
            if file.is_file():
                dir_list_ordered.append(file)
        dir_list_ordered.sort(key=os.path.getmtime, reverse=self._reverse_files)
        return dir_list_ordered

    def please_corrupt_message(self, message):
        print(f"{self._corrupt_message} is set.\nCorrupting message {message}")
        # TODO - add corruption
        return message

    def prepare_message_to_ep(self, message):
        event = Event(send_to="enpoint_1", message=message)
        # pickled_message = pickle.dumps(event)
        pickled_message = jsonpickle.encode(event)
        return pickled_message
