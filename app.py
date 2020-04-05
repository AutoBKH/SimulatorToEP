from Simulator.dir_reader import DirReader
from Simulator.configure import Configure
from Simulator.server import app


def main():
    configuration = Configure()
    DirReader(configuration).start()
    app.run(debug=False, host='0.0.0.0', port=5000)


if __name__ == "__main__":
    main()
