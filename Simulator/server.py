from flask import Flask
from flask import request
from Simulator.configure import Configure
from Simulator.dir_reader import DirReader
from pathlib import Path
import os
import queue

app = Flask(__name__)


@app.route('/')
def sanity():
    return 'SimulatorToEP is up and running\n'


def config():
    if request.method == 'POST':
        if request.is_json:
            print(f"Changing configuration")
            stop_simulator()
            Configure.set_configuration(request.json)
            start_simulator()
            # Configure.set_running_status(True)
            # d = DirReader(Configure)
            # d.start()
            return request.json
        else:
            return str(request.data, "utf-8")
    elif request.method == 'GET':
        conf = Configure.get_configuration()
        return conf


def start_simulator():
    Configure.set_running_status(True)
    d = DirReader(Configure)
    d.start()
    return f"Starting simulator"


def stop_simulator():
    Configure.set_running_status(False)
    return f"Stopping simulator"


def restart_simulator():
    return f"Restarted simulator"


app.add_url_rule('/config', view_func=config, methods=['POST', 'GET'])
app.add_url_rule('/start', view_func=start_simulator, methods=['POST'])
app.add_url_rule('/stop', view_func=stop_simulator, methods=['POST'])
app.add_url_rule('/restart', view_func=restart_simulator, methods=['POST'])



# if __name__ == "__main__":
#     d = DirReader(Path(os.curdir + "/Test/files_from_SP/"), 1)
#     d.start()
#     app.run(debug=True, host='0.0.0.0', port=5000)
