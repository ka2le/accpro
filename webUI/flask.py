#!todo-api/flask/bin/python
from flask import Flask, request

app = Flask(__name__)

@app.route('/hello/test')
def index():
	return 'hello mannen'

@app.route('/status', methods=['GET'])
def webUIBackend():
	#staus is a string with info on the progress
	#when all is done status should return "Complete"
	#to return image status returns an base64 string and this is done with img_base64String to tell the frontend that it is an image
	return status

@app.route('/webUIBackend', methods=['GET'])
def webUIBackend():
	values = request.args.get('values')
	valuesArray = values.split("_");
	startAngle = valuesArray[0]
	endAngle = valuesArray[1]
	nrAngle = valuesArray[2]
	nodes = valuesArray[3]
	levels = valuesArray[4]
	#do all the stuff with the input values

	return "nodes "+str(nodes)+" startAngle "+startAngle #return something else here later

if __name__ == '__main__':
	app.run(debug=True)
