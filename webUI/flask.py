#!todo-api/flask/bin/python
from flask import Flask, request
import sys
sys.path.append("~/accpro")
from mastercontroller import start

app = Flask(__name__)

@app.route('/hello/test')
def index():
	return 'hello mannen'

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
	start(startAngle, endAngle, nrAngle)
	return "nodes "+str(nodes)+" startAngle "+startAngle #return something else here later

@app.route('/p/<int:a_from>,<int:a_to>,<int:a_n>')
def testing(a_from, a_to, a_n):
	start(a_from, a_to, a_n)


if __name__ == '__main__':
	app.run(debug=True)
