class drone:
	def __init__(self, current_drone_url:str) -> None:
		self.current_drone_url = current_drone_url
		self.data = []
		self.neighbour_drones = []
		self.server = ""

	def insert_data(self,cordinate, data):
		data = {
			'cordinate': cordinate,
			'data': data
		}
		self.data.append(data)

	def add_neighbour_drone(self, drone_url):
		self.neighbour_drones.append(drone_url)
		
	def search_data(self, cordinate):
		for data_object in data:
			if data_object['cordinate'] == cordinate:
				return data_object['data']
		return '-1'

