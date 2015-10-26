#!todo-api/flask/bin/python
from flask import Flask, request
import sys, celery, subprocess
#sys.path.append("~/accpro")
from createslaves import create_slaves
from celery import group
import numpy as np
import matplotlib.pyplot as plt
from tasks import airfoil

app = Flask(__name__)

def calc_n_workers(n_angles, max_task_per_worker):
	n = n_angles / max_task_per_worker
	if (n_angles % max_task_per_worker) != 0:
		n += 1
	return n

@app.route('/', methods=['GET'])
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
	#start(startAngle, endAngle, nrAngle)
	return "nodes "+str(nodes)+" startAngle "+startAngle #return something else here later

@app.route('/p/<int:angle_start>,<int:angle_stop>,<int:a_n>', methods=['GET'])
def testing(angle_start, angle_stop, a_n):

	angle_diff = (angle_stop-angle_start)/a_n
    n_workers = calc_n_workers(a_n, 1)
    slave_list = create_slaves(n_workers)

	job = group([airfoil.s(n*angle_diff,0) for n in range(1, a_n+1)])
    result = job.apply_async()

    while result.ready() == False:
        k = 1

    for r in result.get():
    	for angle in r:
    		name = angle['name']
    		data = angle['data'][2:].split()[3:]
    		time = np.array(data[::3], dtype=np.float)
    		lift = np.array(data[1::3], dtype=np.float)
    		drag = np.array(data[2::3], dtype=np.float)
    		fig = plt.figure()
    		pl1 = fig.add_subplot(121)
    		pl1.set_title("Lift force")
    		pl1.plot(time, lift)
    		pl2 = fig.add_subplot(122)
    		pl2.plot(time, drag)
    		pl2.set_title("Drag force")
    		fig.savefig(name + '.png')

    return str(result.get())


if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)