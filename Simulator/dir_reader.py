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


class DirReader(threading.Thread):
    def __init__(self, path: str, delay):
        super().__init__()
        self._path = path
        self._delay = float(delay)
        self._guid = uuid.uuid4()
        print(f"Thread starts id {self._guid}")

    def run(self):
        url = 'http://localhost:5050/publish'
        backup_path = os.curdir + "/Test/backup/"
        guid = uuid.uuid4()
        while True:
            time.sleep(self._delay)
            entries = os.scandir(self._path)
            for entry in entries:
                # TODO - check file endswith
                if entry.is_file():
                    print(f"Found new file {entry.name}. {guid}")
                    f = open(entry.path, "r")
                    contents = json.loads(f.read())
                    f.close()
                    time.sleep(5)
                    response = post(url, data=json.dumps(contents))
                    if response.status_code == HTTPStatus.OK:
                        print(f"Moving file {entry.path} to {backup_path}. {guid}")
                        shutil.move(entry.path, backup_path)
                        print(response.json())




# if __name__ == "__main__":
#     print(os.curdir)
#     d = DirReader(Path(os.curdir + "/Test/files_from_SP/"), 1)
#     d.start()

