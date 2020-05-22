import time
from flask import Flask, request, jsonify
from Simulator.configure import Configure
from Simulator.dir_reader import DirReader
from http import HTTPStatus
from flask_restplus import Api, Resource, fields, marshal_with, reqparse
from werkzeug.contrib.fixers import ProxyFix

app_flask = Flask(__name__)
app = Api(app_flask)


# def is_alive():
@app.doc("something")
class IsAlive(Resource):
    def post(self):
        return jsonify('SimulatorToEP is up and running')

    def get(self):
        return jsonify('SimulatorToEP is up and running')


config = app.model('Config', {"read_from": fields.String(required=True, description="Directory to read from")})

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'user_priority': fields.Integer,
    'custom_greeting': fields.FormattedString('Hey there {username}!'),
    'date_created': fields.DateTime,
    'date_updated': fields.DateTime,
    'links': fields.Nested({
        'friends': fields.Url('user_friends'),
        'posts': fields.Url('user_posts'),
    }),
}
#     ,
#   "write_to": "http://localhost:5050/send_event",
#   "backup_dir": "Test/backup",
#   "errors_dir": "Test/errors",
#   "read_freq_sec": 8,
#   "pass_ratio_percentage": 100,
#   "number_of_duplications": 1,
#   "corrupt_message": false,
#   "read_order_swap": false
# }
#
#     'task': fields.String(required=True, description='The task details')
# })
# def config():
# @app.doc(responses={404: 'Todo not found'}, params={
#     "write_to": "http://localhost:5050/send_event",
#            "backup_dir": "Test/backup",
#            "errors_dir": "Test/errors",
#            "read_freq_sec": "8",
#            "pass_ratio_percentage": "100",
#            "number_of_duplications": "1",
#            "corrupt_message": "False",
#            "read_order_swap": "False"}
#          )
class Config(Resource):
    @app.doc(description='todo_id should be in {0}')
    @app.marshal_with(user_fields)
    def post(self):
        '''Configure simulator'''
        # if request.method == 'POST':
        if request.is_json:
            print(f"Changing configuration")
            Configure.set_configuration(request.json)
            return request.json
        return jsonify("Request not JSON", HTTPStatus.BAD_REQUEST)

    def get(self):
        '''Get simulator configuration'''
    # elif request.method == 'GET':
        conf = Configure.get_configuration()
        return jsonify(conf)
    # else:
    #     return jsonify("Invalid request", HTTPStatus.BAD_REQUEST)


# def start_simulator():
class StartSimulator(Resource):
    def post(self):
        Configure.set_running_status(True)
        DirReader(Configure).start()
        return jsonify(f"Starting simulator")


# def stop_simulator():
class StopSimulator(Resource):
    def post(self):
        Configure.set_running_status(False)
        return jsonify(f"Stopping simulator")


# def restart_simulator():
class RestartSimulator(Resource):
    def post(self):
        Configure.set_running_status(False)
        time.sleep(1)
        Configure.set_running_status(True).start()
        return jsonify("Restarted simulator")


# def shutdown():
class Shutdown(Resource):
    """
    Shuts down the server, only active when running the server locally
    """
    def post(self):
        shutdown_function = request.environ.get("werkzeug.server.shutdown")
        if shutdown_function is None:
            raise ValueError("Cannot shutdown! Server is not running with werkzeug")
        shutdown_function()
        return "Server shutting down"


# app.add_url_rule('/', view_func=is_alive)
# app.add_url_rule('/is_alive', view_func=is_alive)
# app.add_url_rule('/config', view_func=config, methods=['POST', 'GET'])
# app.add_url_rule('/start', view_func=start_simulator, methods=['POST'])
# app.add_url_rule('/stop', view_func=stop_simulator, methods=['POST'])
# app.add_url_rule('/restart', view_func=restart_simulator, methods=['POST'])
# app.add_url_rule("/shutdown", "shutdown", view_func=shutdown, methods=["POST"])


app.add_resource(IsAlive, '/')
app.add_resource(IsAlive, '/is_alive')
app.add_resource(Config, '/config')
app.add_resource(StartSimulator, '/start')
app.add_resource(StopSimulator, '/stop')
app.add_resource(RestartSimulator, '/restart')
app.add_resource(Shutdown, "/shutdown")


if __name__ == "__main__":
    # configuration = Configure()
    # DirReader(configuration).start()
    app_flask.run(debug=True, host='0.0.0.0', port=5000)


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