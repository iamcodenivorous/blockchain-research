import drone as dr
from flask import Flask, request, jsonify
import requests_async as requests
import sys


drone = dr.drone('http://'+sys.argv[1]+':'+sys.argv[2])
app = Flask(__name__)

@app.route('/drone', methods=['GET'])
def drone():
	return jsonify({
		'drone_url': drone.url,
		'data':drone.data,
		'neighbour_drones': drone.neighbour_drones
		})

@app.route('/add-data', methods=['POST'])
def add_data():
	data = request.get_json()
	cordinate = data['cordinate']
	drone_data = data['data']
	drone.add_data(cordinate, drone_data)


if __name__ == '__main__':
    app.run(host= sys.argv[1], port= int(sys.argv[2]),debug=True)

