import sys
from flask import request, jsonify
import requests_async as requests
from droneserver import drone as dr
from droneserver import app
drone = dr.drone('http://'+sys.argv[1]+':'+sys.argv[2])
@app.route('/drone', methods=['GET'])
def drone_data():
	return jsonify({
		'drone_url': drone.current_drone_url,
		'data':drone.data,
		'neighbour_drones': drone.neighbour_drones,
		'server': drone.server
		})


@app.route('/get-connected-drones', methods=['GET'])
def get_connected_drones():
	return jsonify({"drones": drone.neighbour_drones})

@app.route('/add-data', methods=['POST'])
def add_data():
	data = request.get_json()
	cordinate = data['cordinate']
	drone_data = data['data']
	drone.insert_data(cordinate, drone_data)
	return jsonify({'message': 'data added successfully'})


@app.route('/add-neighbour-drone', methods=['POST'])
async def add_neighbour_drone():
	data = request.get_json()
	drone_address = data['drone_address']
	drone.add_neighbour_drone(drone_address)
	res = await requests.post(url = drone_address+'/recieve-neighbour-drone', json={"drone_address": drone.current_drone_url})
	return jsonify({'message': 'drone added successfully'})

@app.route('/recieve-neighbour-drone', methods=['POST'])
def recieve_neighbour_drone():
	data = request.get_json()
	drone_address = data["drone_address"]
	drone.add_neighbour_drone(drone_address)
	return jsonify({'message': 'drone added successfully'})

@app.route('/disconnect_drone', methods=['POST'])
def disconnect_drones():
	data = request.get_json()
	drone_url = data['drone_url']
	drone.remove_neighbour_drone(drone_url)

@app.route('/disconnect-fanet', methods=['GET'])
async def disconnect_fanet():
	if len(drone.neighbour_drones) > 0:
		for dr in drone.neighbour_drones:
			req = await requests.post(url = dr+'/disconnect_drone', json={'drone_url': drone.current_drone_url})
		if len(drone.neighbour_drones) >= 2:
			for i in range(1, len(drone.neighbour_drones)):
				previous_drone_url = drone.neighbour_drones[i - 1]
				current_drone_url = drone.neighbour_drones[i]
				req = await requests.post(url=previous_drone_url+'/add-neighbour-drone', json={'drone_address': current_drone_url})
		drone.neighbour_drones = []
	else:
		return jsonify({'message': 'drone not connected to any network'}), 400
	return jsonify({'message': 'drone disconnected successfully'})

# server routes
@app.route('/add-server', methods=['POST'])
def add_server():
	data = request.get_json()
	server = data['server_url']
	drone.server = server
	return jsonify({'message': 'Server added successfully.'})

@app.route('/remove-server', methods=['GET'])
def remove_server():
	drone.server = ""
	return jsonify({'message': 'Server removed successfully.'})


@app.route('/get-data', methods=['GET'])
def get_data():
	temp = drone.data.copy()
	drone.data = []
	return jsonify({"data": temp})


@app.route('/get-all-data', methods=['GET'])
async def get_all_data():
	data = request.get_json()
	visited = data['visited']
	visited.append(drone.current_drone_url)
	data = [] 
	data.append({drone.current_drone_url: drone.data.copy()})
	if len(drone.neighbour_drones) > 0:
		for dr in drone.neighbour_drones:
			if visited.count(dr) == 0:
				res = await requests.get(dr+'/get-all-data', json={'visited':visited})
				data_json = res.json()
				if len(data_json['data']) > 0:
					for data_element in data_json['data']:
						data.append(data_element)
	drone.data = []
	return jsonify({'data': data.copy()})

