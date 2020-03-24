from Simulator.dir_reader import DirReader
from Simulator.server import app
from Simulator.configure import Configure
from Test.ep_simulator import ep_simulator
from pathlib import Path
from threading import Thread
import os


def start_ep_simulator():
    ep_simulator.run(debug=False, host='0.0.0.0', port=5050)


configuration = Configure()
d = DirReader(configuration)
d.start()
Thread(target=start_ep_simulator).start()
app.run(debug=False, host='0.0.0.0', port=5000)
