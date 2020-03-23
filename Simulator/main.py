from Simulator.dir_reader import DirReader
from Simulator.server import app
from Test.ep_simulator import ep_simulator
import os
from pathlib import Path
from threading import Thread


d = DirReader(Path(os.curdir + "/Test/files_from_SP/"), 1)
d.start()
app.run(debug=False, host='0.0.0.0', port=5000)
