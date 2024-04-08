from flask import Flask, request, jsonify
from flask_cors import CORS

from MultiprocessingCallback import MultiprocessingCallback

app = Flask(__name__)
CORS(app)
multiprocessingCallback = MultiprocessingCallback(app)


@app.route("/startListeners", methods=["POST"])
def startLSLListeners():
    print('im printing yall')
    print(request.json['deviceTypes'])
    multiprocessingCallback.initializeDeviceTypesAndProcesses(request.json['deviceTypes'])
    multiprocessingCallback.startListenerProcesses()
    return "OK"

@app.route("/startListener", methods=["POST"])
def startLSLListener():
    print('im printing yall')
    print(request.json['deviceTypes'])
    multiprocessingCallback.startListenerProcess(request.json['deviceTypes'][0])
    return "OK"

@app.route("/stopListeners", methods=["POST"])
def stopLSLListeners():
    print('im printing yall')
    multiprocessingCallback.stopListenerProcesses()
    return "OK"

@app.route("/stopListener", methods=["POST"])
def stopLSLListener():
    print('im printing yall')
    print(request.json['listenerID'])
    multiprocessingCallback.stopListenerProcess(request.json['listenerID'])
    return "OK"

@app.route("/getListenersStatus", methods=["GET"])
def getListenersStatus():
    print('im printing yall')
    return multiprocessingCallback.getProcessStatus()


if __name__ == "__main_":
	app.run(debug=False, port=5000)