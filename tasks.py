import os, sys, glob, subprocess
from celery import Celery


app = Celery('tasks', backend='amqp', broker='amqp://elias:pass@' + os.environ['master_ip'] + ':5672/geijer')

@app.task
def airfoil(angle):
	subprocess.check_call("./run.sh " + str(angle) + " " + str(angle) +" 1 200 1", shell=True)

	mesh_files = glob.glob('msh/*.msh')
	for mesh in mesh_files:
		subprocess.check_call("python dolphin-convert " + mesh + ' ' + mesh[:-3] + 'xml', shell=True)
'''
	xml_files = glob.glob('msh/*.xml')
	for xml in xml_files:
		subprocess.check_call("./navier_strokes_solver/airfoil 10 0.0001 10. 1 " + "./" + xml, shell=True)
'''