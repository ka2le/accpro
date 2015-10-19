import os, sys, glob, subprocess
from celery import Celery


app = Celery('tasks', backend='amqp', broker='amqp://elias:pass@' + os.environ['master_ip'] + ':5672/geijer')

@app.task
def airfoil(angle):

	print "Generate mesh files for angle " + angle
	subprocess.check_call("./run.sh " + angle + " " + angle +" 1 200 1", shell=True)

	print "Converting the generated mesh files to xml"
	subprocess.check_call("./convert.sh", shell=True))

	print "Run airfiol on every xml file"
	xml_files = glob.glob('msh/*.xml')
	for xml in xml_files:
		subprocess.check_call("./navier_stokes_solver/airfoil 10 0.0001 10. 1 " + "./" + xml, shell=True)
