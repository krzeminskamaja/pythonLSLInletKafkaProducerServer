This is a python server to create LSL stream inlets + Kafka producers for LSL streaming devices that have opened outlets

It listens for LSL data coming through LSL streams and produces this data to its designated Kafka topics, seen as storage

This server can be run in an Anaconda Python (version 3.11.9) environment 
To run:
1) create a new conda environment
2) navigate to this repository folder
3) run "pip install -r requirements.txt" to install all necessary dependencies
4) run "flask run --host=0.0.0.0" to start the server on all IPv4 addresses on the local machine, default port 5000






