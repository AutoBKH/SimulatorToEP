from Simulator.dir_reader import DirReader
from Simulator.server import app
from Simulator.configure import Configure
from Test.ep_simulator import ep_simulator
from Test.spreader_file_creator import create_dummy_ack
from threading import Thread


def start_ep_simulator():
    ep_simulator.run(debug=False, host='0.0.0.0', port=5050)


def local_main():
    configuration = Configure()
    d = DirReader(configuration)
    d.start()
    # Thread(target=start_ep_simulator).start()
    Thread(target=create_dummy_ack, args=("Test/files_from_SP/", 5,)).start()
    app.run(debug=False, host='0.0.0.0', port=5000)


if __name__ == "__main__":
    local_main()
