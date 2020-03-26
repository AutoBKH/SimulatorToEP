from Simulator.dir_reader import DirReader
from Simulator.server import app
from Simulator.configure import Configure
from Test.ep_simulator import ep_simulator
from Test.spreader_file_creator import create_dummy_ack
import threading
from pathlib import Path
from threading import Thread
import os


def start_ep_simulator():
    ep_simulator.run(debug=False, host='0.0.0.0', port=5050)


configuration = Configure()
d = DirReader(configuration)
d.start()
# Thread(target=start_ep_simulator).start()
# x = threading.Thread(target=create_dummy_ack("Test/files_from_SP/", 100), args=(1,))
x = threading.Thread(target=create_dummy_ack, args=("Test/files_from_SP/", 5,))
# x.start()
app.run(debug=False, host='0.0.0.0', port=5000)
