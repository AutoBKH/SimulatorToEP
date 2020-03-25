from flask import Flask
from flask import request
import json

ep_simulator = Flask(__name__)


@ep_simulator.route('/')
def sanity():
    return 'EP Simulator is up and running\n'


@ep_simulator.route('/publish', methods=['POST'])
def publish():
    if request.method == 'POST':
        if request.is_json:
            return request.json
        else:
            return str(request.data, "utf-8")
    else:
        return f"called publish with {request.method}"


@ep_simulator.route('/config', methods=['POST', 'GET'])
def config():
    if request.method == 'POST':
        if request.is_json:
            print(f"Changing configuration")
            return request.json
        else:
            return str(request.data, "utf-8")
    elif request.method == 'GET':
        return f"The current configuration is: "


def about():
    return "about page"


def send_event():
    if request.is_json:
        print(f"Changing configuration")
        # return request.json
        return f"Received send_event"
    else:
        # return str(request.data, "utf-8")
        return f"Received send_event"


ep_simulator.add_url_rule('/config', view_func=config, methods=['POST', 'GET'])
ep_simulator.add_url_rule('/about', view_func=about, methods=['POST', 'GET'])
ep_simulator.add_url_rule('/send_event', view_func=send_event, methods=['POST'])


@ep_simulator.route('/start', methods=['POST'])
def start_simulator():
    if request.method == 'POST':
        return f"Starting simulator"
    else:
        return f"Unrecognized request"


@ep_simulator.route('/stop', methods=['POST'])
def stop_simulator():
    if request.method == 'POST':
        return f"Stopping simulator"
    else:
        return f"Unrecognized request"


@ep_simulator.route('/restart', methods=['POST'])
def restart_simulator():
    if request.method == 'POST':
        return f"Restarted simulator"
    else:
        return f"Unrecognized request"


if __name__ == "__main__":
    ep_simulator.run(debug=False, host='0.0.0.0', port=5050)
