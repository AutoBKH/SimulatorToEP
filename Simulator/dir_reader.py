import threading
import time
import os
import json
import shutil
from requests import post
from pathlib import Path


class DirReader(threading.Thread):
    def __init__(self, thread_id, path: str, delay):
        super().__init__()
        self._thread_id = thread_id
        self._path = path
        self._delay = float(delay)

    def run(self):
        print(f"Thread starts id {str(self._thread_id)}")
        url = 'http://localhost:5000/publish'
        while True:
            time.sleep(self._delay)
            entries = os.scandir(self._path)
            for entry in entries:
                # TODO - check file endswith
                if entry.is_file():
                    print(entry.name)
                    f = open(entry.path, "r")
                    contents = json.loads(f.read())
                    response = post(url, data=json.dumps(contents))
                    print(response.json())
                    print(contents)
                    
            print(f"Hello from MyThread {self._thread_id}: ")


print(os.curdir)
d = DirReader(123, Path(os.curdir + "/Test/files_from_SP/"), 1)
d.start()

