from flask import Flask,request
import os
from subprocess import Popen, CREATE_NEW_CONSOLE, DEVNULL
app = Flask(__name__)
from flask_cors import CORS
CORS(app)
@app.route('/start/blockchain', methods=['POST'])
def start_blockchain():
	data = request.get_json()
	server_ip = data['ip']
	server_port = data['port']
	args = r'.\blockchainserver\blockchain_server.py'
	p = Popen(['python', args], creationflags=CREATE_NEW_CONSOLE)
	return 'server started successfully....'

@app.route('/start/drone', methods=['POST'])
def start_drone():
	data = request.get_json()
	drone_ip = data['ip']
	drone_port = data['port']
	args = r'.\droneserver\drone_server.py'
	p = Popen([python, args, drone_ip, str(drone_port)], creationflags=CREATE_NEW_CONSOLE)
	return "drone started successfully...."

if __name__ == '__main__':
	app.run(debug=True)