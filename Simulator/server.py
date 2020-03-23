from flask import Flask
from flask import request
from Simulator.dir_reader import DirReader
from pathlib import Path
import os

app = Flask(__name__)


@app.route('/')
def sanity():
    return 'SimulatorToEP is up and running\n'


@app.route('/config', methods=['POST', 'GET'])
def config():
    if request.method == 'POST':
        if request.is_json:
            print(f"Changing configuration")
            return request.json
        else:
            return str(request.data, "utf-8")
    elif request.method == 'GET':
        return f"The current configuration is: "


@app.route('/start', methods=['POST'])
def start_simulator():
    if request.method == 'POST':
        return f"Starting simulator"
    else:
        return f"Unrecognized request"


@app.route('/stop', methods=['POST'])
def stop_simulator():
    if request.method == 'POST':
        return f"Stopping simulator"
    else:
        return f"Unrecognized request"


@app.route('/restart', methods=['POST'])
def restart_simulator():
    if request.method == 'POST':
        return f"Restarted simulator"
    else:
        return f"Unrecognized request"


# if __name__ == "__main__":
#     d = DirReader(Path(os.curdir + "/Test/files_from_SP/"), 1)
#     d.start()
#     app.run(debug=True, host='0.0.0.0', port=5000)
