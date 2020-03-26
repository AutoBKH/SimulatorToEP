from mimesis.schema import Field, Schema
from mimesis.enums import FileType
from mimesis import File
from pathlib import Path
from random import randint
import json
import time


def create_dummy_ack(path, loops):
    _ = Field('en')
    dummy_ack = Schema(
        lambda: {
            "message_id": _('uuid'),
            "timestamp": str(_('datetime'))
        }
    )

    for x in range(loops):
        num_of_files = randint(1, 30)
        interval_sec = randint(4, 10)
        dummy_data = dummy_ack.create(num_of_files)
        file_fake = File()
        for msg in dummy_data:
            f = open(Path(path + file_fake.file_name(file_type=FileType.TEXT)), "w")
            f.write(json.dumps(msg))
            f.close()
        time.sleep(interval_sec)


if __name__ == "__main__":
    create_dummy_ack("Test/files_from_SP/", 3)
