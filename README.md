# SimulatorToEP
Simulate channel from spreader to event publisher using a REST API for configuring channel quality.
The simulator reads files from "read_from" at "read_freq_sec" frequency and sends each file content as body to "write_to".
After reading each file, it'll be moved to "backup_dir"

The simulator can be ran locally, it will use a aditional flask server which will simulator the Event Publisher server.

In order to run with simulator locally:
1. put files in the "read_from" directory
2. verify that "backup_dir" exist
3. run the local_main.py. 

RESTFUL commands:

GET  http://localhost:5000/config

POST http://localhost:5000/config
{\
  "read_from": "Test/files_from_SP",\
  "write_to": "http://localhost:5050/publish",\
  "backup_dir": "Test/backup2",\
  "read_freq_sec": 5,\
  "pass_ratio_percentage": 100,\
  "corrupt": false,\
  "read_order_swap": false,\
  "duplicate_messages": true\
}

POST http://localhost:5000/start

POST http://localhost:5000/stop

