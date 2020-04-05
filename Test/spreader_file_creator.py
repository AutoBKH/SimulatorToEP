from mimesis.schema import Field, Schema
from mimesis.enums import FileType
import mimesis
from pathlib import Path
from random import randint
import json
import time


def create_dummy_ack(path, loops, num_files: int, interval_sec: int, random_selection=False):
    _ = Field('en')
    dummy_ack = Schema(
        lambda: {
            "message_id": _('uuid'),
            "timestamp": str(_('datetime'))
        }
    )

    if random_selection:
        _num_of_files = randint(1, 30)
        _interval_sec = randint(4, 10)
    else:
        _num_of_files = num_files
        _interval_sec = interval_sec

    for x in range(loops):
        dummy_data = dummy_ack.create(_num_of_files)
        file_fake = mimesis.File()
        for msg in dummy_data:
            f = open(Path(path + "/" + file_fake.file_name(file_type=FileType.TEXT)), "w")
            f.write(json.dumps(msg))
            f.close()
        time.sleep(interval_sec)


def create_dummy_empty(path, loops, num_files: int, interval_sec: int, random_selection=False):

    if random_selection:
        _num_of_files = randint(1, 30)
        _interval_sec = randint(4, 10)
    else:
        _num_of_files = num_files
        _interval_sec = interval_sec

    for x in range(loops):
        for y in range(num_files):
            file_fake = mimesis.File()
            f = open(Path(path + "/" + file_fake.file_name(file_type=FileType.TEXT)), "w")
            f.close()
        time.sleep(interval_sec)


if __name__ == "__main__":
    create_dummy_ack("Test/files_from_SP/", loops=2, num_files=10, interval_sec=61)
