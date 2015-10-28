#!todo-api/flask/bin/python
from flask import Flask, request
import os, sys, celery, subprocess, base64, glob, matplotlib
from subprocess import check_call
from createslaves import create_slaves
from celery import group
from tasks import airfoil
import numpy as np
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from novaclient.client import Client


app = Flask(__name__)

def calc_n_workers(n_angles, max_task_per_worker):
	n = n_angles / max_task_per_worker
	if (n_angles % max_task_per_worker) != 0:
		n += 1
	return n

@app.route('/status', methods=['GET'])
def status():
	png_files = glob.glob('plots/*.png')
	for png_f in png_files:
		with open(png_f, 'rb') as f:
			encoded_png = base64.b64encode(f.read())
		check_call("sudo mv " + png_f + " plots/finished/" + png_f[6:], shell=True)
		break
	image = 'img_' + encoded_png
	return image

@app.route('/webUIBackend', methods=['GET'])
def backend():

	startAngle = int(request.args.get('startAngle'))
	endAngle = int(request.args.get('endAngle'))
	nrAngle = int(request.args.get('nrAngle'))
	max_task_per_worker = int(request.args.get('nodes'))
	levels = int(request.args.get('levels'))

	config = {'username':os.environ['OS_USERNAME'],
        'api_key':os.environ['OS_PASSWORD'],
        'project_id':os.environ['OS_TENANT_NAME'],
        'auth_url':os.environ['OS_AUTH_URL']}

	nc = Client('2',**config)

	workers = sorted(nc.servers.list(search_opts={'name': 'lundestance-slave'}), key=lambda w: w.name)
	n_workers_running = len(workers)
	n_workers = calc_n_workers(nrAngle, max_task_per_worker)
	print '%d workers running, %d workers are needed for the task start=%d, stop=%d, n=%d, max_task_per_worker=%d' % (n_workers_running, n_workers, startAngle, endAngle, nrAngle, max_task_per_worker)

	# Scale up
	if n_workers_running < n_workers:
		print 'Adding %d workers' % (n_workers-n_workers_running)
		workers = create_slaves(n_workers-n_workers_running)

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
	angles = [startAngle + n*angle_diff for n in range(1, nrAngle+1)]
	print 'Sending task for angles: %s' % str(angles)
	job = group([airfoil.s(a,levels) for a in angles])
	result = job.apply_async()

	while result.ready() == False:
		k = 1
	print 'Task done, now create plots'
	for r in result.get():
		for angle in r:
			name = angle['name']
			data = angle['data'][2:].split()[3:]
			time = np.array(data[::3], dtype=np.float)
			lift = np.array(data[1::3], dtype=np.float)
			drag = np.array(data[2::3], dtype=np.float)
			fig = plt.figure()
			pl1 = fig.add_subplot(211)
			pl1.set_title("Lift force")
			pl1.plot(time, lift)
			pl2 = fig.add_subplot(212)
			pl2.plot(time, drag)
			pl2.set_title("Drag force")
			fig.savefig('plots/' + name + '.png')

	return "OK"

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)