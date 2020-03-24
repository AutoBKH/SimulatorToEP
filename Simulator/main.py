from Simulator.dir_reader import DirReader
from Simulator.configure import Configure
from Simulator.server import app
from Test.ep_simulator import ep_simulator
import os
from pathlib import Path
from threading import Thread
import queue

q = queue.Queue()
configuration = Configure()
d = DirReader(configuration)
d.start()
q.put("something in the queue")
app.run(debug=False, host='0.0.0.0', port=5000)
