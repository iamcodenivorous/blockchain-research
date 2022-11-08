from droneserver import app
import sys
if __name__ == '__main__':
	app.run(host= sys.argv[1], port= int(sys.argv[2]),debug=False)