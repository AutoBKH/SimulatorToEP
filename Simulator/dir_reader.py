import threading
import time
import os
import json
import shutil
from requests import post
from pathlib import Path
from http import HTTPStatus
import uuid
import time
from Simulator.configure import Configure


class DirReader(threading.Thread):
    def __init__(self, config):
        super().__init__()
        self._is_enabled = config.get_running_status()
        self._read_from = config.get_configuration().get("read_from")
        self._write_to = config.get_configuration().get("write_to")
        self._backup_dir = config.get_configuration().get("backup_dir")
        self._delay = config.get_configuration().get("read_freq_sec")
        self._guid = uuid.uuid4()
        print(f"Thread starts id {self._guid}")

    def run(self):
        url = self._write_to
        guid = uuid.uuid4()
        while Configure.get_running_status():
            # msg = self.queue.get()
            # print(msg)
            time.sleep(self._delay)
            entries = os.scandir(self._read_from)
            for entry in entries:
                # TODO - check file endswith
                if entry.is_file():
                    print(f"Found new file {entry.name}. {guid}")
                    f = open(entry.path, "r")
                    contents = json.loads(f.read())
                    f.close()
                    time.sleep(1)
                    response = post(url, data=json.dumps(contents))
                    if response.status_code == HTTPStatus.OK:
                        print(f"Moving file {entry.path} to {self._backup_dir}. {guid}")
                        shutil.move(entry.path, self._backup_dir)
                        print(response.json())




# if __name__ == "__main__":
#     print(os.curdir)
#     d = DirReader(Path(os.curdir + "/Test/files_from_SP/"), 1)
#     d.start()

