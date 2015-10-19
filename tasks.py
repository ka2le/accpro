import os, sys, glob, subprocess
from celery import Celery


app = Celery('tasks', backend='amqp', broker='amqp://elias:pass@' + os.environ['master_ip'] + ':5672/geijer')

@app.task
def airfoil(angle):

	print "Generate mesh files for angle " + angle
	subprocess.check_call("./run.sh " + angle + " " + angle +" 1 200 1", shell=True)

	print "Converting the generated mesh files to xml"
	mesh_files = glob.glob('msh/*.msh')
	print "Mesh files to convert: " + str(mesh_files)
	for mesh in mesh_files:
		print "Converting " + mesh
		cmd = "dolfin-convert " + mesh + ' ' + mesh[:-3] + 'xml'
		print "Command to be run: " + cmd
		subprocess.check_call(cmd, shell=True)

	print "Run airfiol on every xml file"
	xml_files = glob.glob('msh/*.xml')
	for xml in xml_files:
		subprocess.check_call("./navier_stokes_solver/airfoil 10 0.0001 10. 1 " + "./" + xml, shell=True)
