from flask import Flask,request, render_template
import os
from subprocess import Popen, CREATE_NEW_CONSOLE, DEVNULL
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hgftite565etdyrdi56d@@46747uf'

from flask_cors import CORS
CORS(app)

@app.route('/start/server', methods=['POST'])
def start_blockchain():
	data = request.get_json()
	server_ip = data['ip']
	server_port = data['port']
	args = r'.\blockchain_server.py'
	p = Popen(['python', args, server_ip, str(server_port)], shell=True)
	return 'server started successfully....'

@app.route('/start/drone', methods=['POST'])
def start_drone():
	data = request.get_json()
	drone_ip = data['ip']
	drone_port = data['port']
	args = r'.\drone_server.py'
	p = Popen(['python', args, drone_ip, str(drone_port)], shell=True)
	return "drone started successfully...."

@app.route('/', methods=['GET'])
def index():
	 return render_template('index.html')

if __name__ == '__main__':
	app.run(debug=False)