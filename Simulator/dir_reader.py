import threading
import os
import json
import shutil
import uuid
import time
from random import random, randint
import jsonpickle
from requests import post
from pathlib import Path
from http import HTTPStatus
from Simulator.configure import Configure
from Simulator.event import Event

# TODO 0. See other TODOs in code
# TODO 1. Add logging
# TODO 2. Should set max to files read each time get_dir_list_ordered?
# TODO 3. if file content with error, send to error specific directory


def prepare_message_to_ep(message):
    # TODO - change the content of the event.
    event = Event(send_to="enpoint_" + str(randint(0, 100)), message=message)
    pickled_message = jsonpickle.encode(event)
    return pickled_message


class DirReader(threading.Thread):
    def __init__(self, config):
        super().__init__()
        self._read_from = config.get_configuration().get("read_from")
        self._write_to = config.get_configuration().get("write_to")
        self._backup_dir = config.get_configuration().get("backup_dir")
        self._errors_dir = config.get_configuration().get("errors_dir")
        self._corrupt_message = config.get_configuration().get("corrupt_message")
        self.read_freq_sec = config.get_configuration().get("read_freq_sec")
        self._reverse_files = config.get_configuration().get("read_order_swap")
        self._duplicate_message = config.get_configuration().get("duplicate_message")
        self._pass_ratio = config.get_configuration().get("pass_ratio_percentage")
        self._number_of_duplications = config.get_configuration().get("number_of_duplications")
        self._guid = uuid.uuid4()
        print(f"Thread starts id {self._guid}")

    def run(self):
        url = self._write_to
        guid = uuid.uuid4()
        while Configure.get_running_status():
            try:
                for file in self.get_dir_list_ordered():
                    print(f"Found new file {file}. {guid}")
                    try:
                        if self.is_send_file():
                            contents = self.prepare_file_content(file)
                            if contents is None:
                                self.move_file(file, self._errors_dir)
                            else:
                                response = post(url, data=contents)
                                if response.status_code == HTTPStatus.OK:
                                    print(f"Moving file {file} to {self._backup_dir}. {guid}")
                                    self.move_file(file, self._backup_dir)
                                    print(response.json())
                                for n in range(1, self._number_of_duplications):
                                    response = post(url, data=contents)
                                    if response.status_code == HTTPStatus.OK:
                                        print(f"Sent duplicated message")
                                        print(response.json())
                                    time.sleep(0.5)
                        else:
                            self.move_file(file, self._backup_dir)
                            print(f"Skip...Moving file {file} to {self._backup_dir}. {guid}")
                    except Exception as e:
                        print(f"Exception occurred {e}")
                    if Configure.get_running_status() is False:
                        return
            except Exception as e:
                print(f"Exception occurred {e}")
                return
            time.sleep(self.read_freq_sec)

    def is_send_file(self):
        """
        Use random to calculate pass ratio. Given in percentage.
        """
        return random() <= (self._pass_ratio / 100)

    def get_dir_list_ordered(self):
        """
        Return ordered list by creation time of files in directory.
        reverse_files = False --> FIFO
        reverse_files = True --> LIFO
        """
        dir_list_ordered = []
        try:
            for file in Path(self._read_from).iterdir():
                # TODO - should check files of specific type?
                if file.is_file():
                    dir_list_ordered.append(file)
            dir_list_ordered.sort(key=os.path.getmtime, reverse=self._reverse_files)
        except Exception as e:
            print(f"Exception occurred {e}")
        finally:
            return dir_list_ordered

    def please_corrupt_message(self, message):
        print(f"{self._corrupt_message} is set.\nCorrupting message {message}")
        # TODO - add corruption
        return message

    def prepare_file_content(self, file):
        contents = None
        f = open(str(file), "r")
        try:
            contents = json.loads(f.read())
        except ValueError as e:
            print(f"Content is not a JSON")
        finally:
            f.close()

        if contents is not None:
            if self._corrupt_message:
                contents = self.please_corrupt_message(contents)
            contents = prepare_message_to_ep(contents)
        return contents

    def move_file(self, file, dest_dir):
        """
        Before moving file, check if exists and delete
        """
        try:
            if os.path.exists(dest_dir + "/" + str(file.name)):
                os.remove(dest_dir + "/" + str(file.name))
            shutil.move(str(file), dest_dir)
        except Exception as e:
            print(f"Exception occurred {e}")
