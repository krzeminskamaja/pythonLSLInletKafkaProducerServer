from flask import Flask, request, jsonify

from flask_cors import CORS
import json

from MultiprocessingCallback import MultiprocessingCallback

app = Flask(__name__)
CORS(app)

@app.route("/startLSLListeners", methods=["POST"])
def startLSLListeners():
    print('im printing yall')
    print(request.json['deviceTypes'])
    multiprocessingCallback = MultiprocessingCallback()
    multiprocessingCallback.startListenerProcesses(request.json['deviceTypes'])
    return "OK"

if __name__ == "__main_":
	app.run(debug=False, port=5000)