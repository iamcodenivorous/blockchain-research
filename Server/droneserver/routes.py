
from flask import Flask, request, jsonify
import requests_async as requests
from droneserver import drone as dr
from droneserver import app
import sys

drone = dr.drone('http://'+sys.argv[1]+':'+sys.argv[2])
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