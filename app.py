from flask import Flask, request, jsonify


from MultiprocessingCallback import MultiprocessingCallback

app = Flask(__name__)


@app.route("/startListeners", methods=["POST"])
def startLSLListeners():
    print('im printing yall')
    print(request.json['deviceTypes'])
    multiprocessingCallback = MultiprocessingCallback(app)
    multiprocessingCallback.initializeDeviceTypesAndProcesses(request.json['deviceTypes'])
    multiprocessingCallback.startListenerProcesses()
    return "OK"

@app.route("/stopListeners", methods=["POST"])
def stopLSLListeners():
    print('im printing yall')
    print(request.json['deviceTypes'])
    multiprocessingCallback = MultiprocessingCallback(app)
    multiprocessingCallback.stopListenerProcesses()
    return "OK"

if __name__ == "__main_":
	app.run(debug=False, port=5000)