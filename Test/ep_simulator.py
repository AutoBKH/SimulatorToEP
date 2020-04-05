from flask import Flask, request, jsonify
import jsonpickle

ep_simulator = Flask(__name__)


def is_alive():
    return jsonify('EP Simulator is_alive')


def send_event():
    if request.is_json:
        print(f"called send_event")
        return jsonify(request.json)
    else:
        unpickle = jsonpickle.decode(request.data)
        print(unpickle)
        return jsonify(message=unpickle.message,
                       send_to=unpickle.send_to)


def publish():
    if request.method == 'POST':
        if request.is_json:
            return jsonify(request.json)
        else:
            return jsonify(str(request.data, "utf-8"))
    else:
        return jsonify("called publish with {request.method}")


def shutdown():
    """
    Shuts down the server, only active when running the server locally
    """
    shutdown_function = request.environ.get("werkzeug.server.shutdown")
    if shutdown_function is None:
        raise ValueError("Cannot shutdown! Server is not running with werkzeug")
    shutdown_function()
    return "Server shutting down"


ep_simulator.add_url_rule('/', view_func=is_alive)
ep_simulator.add_url_rule('/is_alive', view_func=is_alive)
ep_simulator.add_url_rule('/send_event', view_func=send_event, methods=['POST'])
ep_simulator.add_url_rule('/publish', view_func=publish, methods=['POST'])
ep_simulator.add_url_rule("/shutdown", "shutdown", view_func=shutdown, methods=["POST"])


if __name__ == "__main__":
    ep_simulator.run(debug=False, host='0.0.0.0', port=5050)
