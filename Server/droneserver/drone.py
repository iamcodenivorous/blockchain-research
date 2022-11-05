class drone:
	def __init__(self, current_node_url:str):
		self.url = current_node_url
		self.data = []
		self.neighbour_drones = []

	def insert_data(cordinate, data):
		data = {
			'cordinate': cordinate,
			'data': data
		}
		self.data.append(data)

	def add_neighbour_drone(drone_url):
		self.neighbour_drones.append(drone_url)
		
	def search_data(cordinate):
		for data_object in data:
			if data_object['cordinate'] == cordinate:
				return data_object['data']
		return '-1'

