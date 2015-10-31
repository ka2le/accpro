import os, sys, celery, subprocess, base64, glob, matplotlib
import numpy as np
from createworkers import create_workers
from subprocess import check_call
from flask import Flask, request
from tasks import airfoil
from celery import group
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from novaclient.client import Client

app = Flask(__name__)


#Flask app that gets input from front-end and returns result via ajax
#Front-end calls /status every 10 second


# Calculates and returns how many workers that are needed based on max_task_per_worker
def calc_n_workers(n_angles, max_task_per_worker):
	n = n_angles / max_task_per_worker
	if (n_angles % max_task_per_worker) != 0:
		n += 1
	return n


# Creates a plot containing two subplots and stores it on disk
def plot(name, time, lift, drag):
	fig = plt.figure()
	fig.suptitle(name, fontsize=20)
	pl1 = fig.add_subplot(211)
	pl1.set_title("Lift force")
	pl1.plot(time, lift)
	pl2 = fig.add_subplot(212)
	pl2.plot(time, drag)
	pl2.set_title("Drag force")
	fig.savefig('plots/' + name + '.png')
	

# Takes input from frontend. Add or removes workers if necessary
# Send tasks to workers
@app.route('/webUIBackend', methods=['GET'])
def backend():

	worker_prefix = os.environ['worker_prefix']

	# Get input from front-end
	startAngle = int(request.args.get('startAngle'))
	endAngle = int(request.args.get('endAngle'))
	nrAngle = int(request.args.get('nrAngle'))
	nodes = int(request.args.get('nodes'))
	levels = int(request.args.get('levels'))
	max_task_per_worker = int(request.args.get('maxAngles'))

	# Check if all inputs are valid
	if not (0 <= startAngle <= 180):
		startAngle = 0 
	if not (0 <= endAngle <= 180):
		endAngle = 10
	if not (0 < nrAngle <= 75):
		nrAngle = 1
	if not (100 <= nodes <= 300):
		nodes = 200
	if not (0 <= levels <= 5):
		levels = 0
	if not (1 <= max_task_per_worker <= 20):
		max_task_per_worker = 1

	config = {'username':os.environ['OS_USERNAME'],
        'api_key':os.environ['OS_PASSWORD'],
        'project_id':os.environ['OS_TENANT_NAME'],
        'auth_url':os.environ['OS_AUTH_URL']}

	nc = Client('2',**config)

	# Get all workers which name starts with worker_prefix to a list and sort the list by the names of the workers
	workers = sorted(nc.servers.list(search_opts={'name': worker_prefix}), key=lambda w: w.name)
	n_workers_running = len(workers)

	n_workers = calc_n_workers(nrAngle, max_task_per_worker)
	print '%d workers running, %d workers are needed for the task start=%d, stop=%d, n=%d, max_task_per_worker=%d' % (n_workers_running, n_workers, startAngle, endAngle, nrAngle, max_task_per_worker)

	# Scale up
	if n_workers_running < n_workers:
		print 'Adding %d workers' % (n_workers-n_workers_running)
		workers = create_workers(n_workers-n_workers_running)

	# Scale down
	elif n_workers_running > n_workers:
		print 'Killing %d workers' % len(workers[n_workers:])
		check_call("sudo rabbitmqctl stop_app", shell=True)
		check_call("sudo rabbitmqctl force_reset", shell=True)

		workers_to_kill = workers[n_workers:]
		workers = workers[:n_workers]
		for w in workers_to_kill:
			w.delete()

		check_call("sudo rabbitmqctl start_app", shell=True)
		check_call("sudo rabbitmqctl add_user elias pass", shell=True)
		check_call("sudo rabbitmqctl add_vhost geijer", shell=True)
		check_call('sudo rabbitmqctl set_permissions -p geijer elias ".*" ".*" ".*"', shell=True)

	angle_diff = (endAngle-startAngle)/nrAngle

	# Generate a list from input of all angles to be calculated
	angles = [startAngle + n*angle_diff for n in range(1, nrAngle+1)]


	print 'Sending task for angles: %s' % str(angles)
	job = group([airfoil.s(a, nodes, levels) for a in angles])
	result = job.apply_async()

	while result.ready() == False:
		k = 1

	images = ''

	print 'Task done, now create plots'
	for r in result.get():
		for angle in r:
			name = angle['name']
			print "NAME OF ANGLE:   " + name
			data = angle['data'][2:].split()[3:]
			time = np.array(data[::3], dtype=np.float)
			lift = np.array(data[1::3], dtype=np.float)
			drag = np.array(data[2::3], dtype=np.float)
			plot(name, time, lift, drag)
			fname = 'plots/' + name + '.png'
			with open(fname, 'rb') as f:
				images = images + '_' + base64.b64encode(f.read())
			check_call("sudo rm " + fname, shell=True)

	return 'data' + images


if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)