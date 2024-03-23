This is a python server to create LSL stream inlets + Kafka producers for LSL streaming devices that have opened outlets

It will be refactored into a thread pool to serve the following functionality:
1) user will send a request with the following data 
[{
	LSL: true/false,
	isParent: true/false
	deviceType: text/enum
	outletName: (or do we want all 3?)
  port: int (for zeroMQ)
	sessionID: "stringstrings"
},
{
	LSL: true/false,
	isParent: true/false
	deviceType: text/enum
	outletName: (or do we want all 3?)
  port: int (for zeroMQ)
	sessionID: "stringstrings"
},...]
2) for each of the objects in the collection, a proper listening LSL stream inlet/Kafka producer process will start

The server will have POST endpoints to receive the start and stop listening requests. 
The server ensures all processes can share memory correctly.






