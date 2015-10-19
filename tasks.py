import os, sys, glob
from subprocess import CalledProcessError, check_output, check_call
from celery import Celery
from dolfin_convert import gmsh2xml


app = Celery('tasks', backend='amqp', broker='amqp://elias:pass@' + os.environ['master_ip'] + ':5672/geijer')

@app.task
def airfoil(angle):

	print "Generate mesh files for angle " + angle
	check_call("./run.sh " + angle + " " + angle +" 1 200 1", shell=True)

	print "Converting the generated mesh files to xml"
	msh_files = glob.glob('msh/*.msh')
	for msh in msh_files:
		gmsh2xml(msh, msh[:-3] + 'xml')
		print "Finished convert " + msh

	print "Run airfiol on every xml file"
	xml_files = glob.glob('msh/*.xml')
	for xml in xml_files:
		try:
			check_output(["./navier_stokes_solver/airfoil", "10", "0.0001", "10.", "1", "./" + xml])
		except CalledProcessError as e:
			print e.returncode

