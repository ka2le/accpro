import os, sys, glob
from subprocess import CalledProcessError, check_output, check_call
from celery import Celery
from dolfin_convert import gmsh2xml

app = Celery('tasks', backend='amqp', broker='amqp://elias:pass@' + os.environ['master_ip'] + ':5672/geijer')
app.conf.CELERY_ACKS_LATE = True
app.conf.CELERYD_PREFETCH_MULTIPLIER = 1

@app.task
def airfoil(angle, nodes, levels):

	results = []

	print "Generate mesh files for angle " + str(angle)
	check_call("./run.sh " + str(angle) + " " + str(angle) +" 1 " + str(nodes) + " " + str(levels) , shell=True)

	print "Converting the generated mesh files to xml"
	msh_files = glob.glob('msh/*.msh')
	for msh in msh_files:
		gmsh2xml(msh, msh[:-3] + 'xml')
		print "Finished convert " + msh

	print "Run airfiol on every xml file"
	xml_files = glob.glob('msh/*.xml')
	for xml in xml_files:
		try:
			check_call("sudo ./navier_stokes_solver/airfoil 10 0.0001 10. 0.2 ./" + xml, shell=True)
			with open("results/drag_ligt.m", 'r') as f:
				result = f.read()
			results.append({'name':xml[4:-4], 'data':result})

		except CalledProcessError as e:
			print e.returncode

	print "Delete .msh files:"
	check_call("sudo rm msh/*", shell=True)
	print "Delete .geo files:"
	check_call("sudo rm geo/*", shell=True)
	return results