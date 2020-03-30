import os
from flask import Flask, request, jsonify
from pathlib import Path
from Simulator.configure import Configure
from Simulator.dir_reader import DirReader

app = Flask(__name__)


def is_alive():
    return jsonify('SimulatorToEP is up and running')


def config():
    if request.method == 'POST':
        if request.is_json:
            print(f"Changing configuration")
            Configure.set_configuration(request.json)
            return request.json
        # else:
        #     Configure.set_configuration(jsonify(request.data))
        #     return str(request.data, "utf-8")
    elif request.method == 'GET':
        conf = Configure.get_configuration()
        return jsonify(conf)


def start_simulator():
    Configure.set_running_status(True)
    d = DirReader(Configure)
    d.start()
    return jsonify(f"Starting simulator")


def stop_simulator():
    Configure.set_running_status(False)
    return jsonify(f"Stopping simulator")


def restart_simulator():
    return jsonify("Restarted simulator")


def shutdown():
    """
    Shuts down the server, only active when running the server locally
    """
    shutdown_function = request.environ.get("werkzeug.server.shutdown")
    if shutdown_function is None:
        raise ValueError("Cannot shutdown! Server is not running with werkzeug")
    shutdown_function()
    return "Server shutting down"


app.add_url_rule('/', view_func=is_alive)
app.add_url_rule('/is_alive', view_func=is_alive)
app.add_url_rule('/config', view_func=config, methods=['POST', 'GET'])
app.add_url_rule('/start', view_func=start_simulator, methods=['POST'])
app.add_url_rule('/stop', view_func=stop_simulator, methods=['POST'])
app.add_url_rule('/restart', view_func=restart_simulator, methods=['POST'])
app.add_url_rule("/shutdown", "shutdown", view_func=shutdown, methods=["POST"])

if __name__ == "__main__":
    d = DirReader(Path(os.curdir + "/Test/files_from_SP/"), 1)
    d.start()
    app.run(debug=True, host='0.0.0.0', port=5000)


"""
class ServerHandler

__init
host
port
debug
logger
self.server_app = _create_server

_create_server(self) --> Flask:
    flask_server = Flask(__name__)
    self.register_flask_rules(flask_server)
    return flask_server


def run_local_server()
    self.server_app.add_url_rule("/shutdown
    self.server_app.run(....)
    
def register_flask_rules(self, flask_server: Flask)
    flask_server.add_url_rule("/", None, self.is_alive)
    flask_server.add_url_rule("/is_alive", is_alive, self.is_alive)
    flask_server.add_url_rule...


"""