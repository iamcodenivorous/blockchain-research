from flask import Flask,request
import os
app = Flask(__name__)

@app.route('/start/blockchain', methods=['POST'])
def start_blockchain():
	data = request.get_json()
	server_ip = data['ip']
	server_port = data['port']
	os.system(f'flask --app blockchainserver/blockchain_server run  --host {server_ip} --port {server_port}')
	return "blockchain started successfully"
@app.route('/start/drone', methods=['POST'])
def start_drone():
	data = request.get_json()
	client_ip = data['ip']
	client_port = data['port']
	subprocess.call('python ./droneserver/drone_server.py '+ client_ip +' ' + str(client_port))
	return "drone started successfully"

if __name__ == '__main__':
	app.run(debug=True)