import os, sys, glob
from subprocess import CalledProcessError, check_call
from celery import Celery
from dolfin_convert import gmsh2xml

app = Celery('tasks', backend='amqp', broker='amqp://elias:pass@' + os.environ['master_ip'] + ':5672/geijer')
app.conf.CELERY_ACKS_LATE = True
app.conf.CELERYD_PREFETCH_MULTIPLIER = 1


# Takes one angle as input as an integer, which will generate mesh files, convert them to xml and then run airfoil on them
@app.task
def airfoil(angle, nodes, levels):
	subprocess.check_call("sudo rm msh/*", shell=True)
	subprocess.check_call("sudo rm geo/*", shell=True)
	
	results = []

	print "Generate mesh files for angle " + str(angle)
	check_call("./run.sh " + str(angle) + " " + str(angle) +" 1 " + str(nodes) + " " + str(levels) , shell=True)

	print "Converting the generated mesh files to xml"
	msh_files = glob.glob('msh/r*a' + str(angle) + 'n*.msh')
	for msh in msh_files:
		gmsh2xml(msh, msh[:-3] + 'xml')
		print "Finished convert " + msh
		#check_call("sudo rm " + msh, shell=True)
		#print "Deleted mesh: " + msh
		#check_call("sudo rm geo/" + msh[6:-3] + 'geo' , shell=True)
		#print "Deleted geo: geo/" + msh[6:-3] + 'geo'

	print "Run airfiol on every xml file"
	xml_files = glob.glob('msh/a*' + str(angle) 'n*.xml')
	for xml in xml_files:
		try:
			check_call("sudo ./navier_stokes_solver/airfoil 10 0.0001 10. 0.2 ./" + xml, shell=True)
			check_call("sudo rm " + xml, shell=True)
			print "Deleted xml: " + xml
			with open("results/drag_ligt.m", 'r') as f:
				result = f.read()
			results.append({'name':xml[4:-4], 'data':result})

		except CalledProcessError as e:
			print e.returncode

	return results