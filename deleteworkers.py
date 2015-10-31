import os, subprocess
from novaclient.client import Client
 
# This script is used for debugging when you want to delete all workers and start from scratch

config = {'username':os.environ['OS_USERNAME'],
          'api_key':os.environ['OS_PASSWORD'],
          'project_id':os.environ['OS_TENANT_NAME'],
          'auth_url':os.environ['OS_AUTH_URL'],
           }
 
nova = Client('2',**config)

worker_prefix = os.environ['worker_prefix']

instances = nova.servers.list(search_opts={'name': worker_prefix})

subprocess.check_call("sudo rabbitmqctl stop_app", shell=True)
subprocess.check_call("sudo rabbitmqctl force_reset", shell=True)

for a in instances: 
	a.delete()    

subprocess.check_call("sudo rabbitmqctl start_app", shell=True)
subprocess.check_call("sudo rabbitmqctl add_user elias pass", shell=True)
subprocess.check_call("sudo rabbitmqctl add_vhost geijer", shell=True)
subprocess.check_call('sudo rabbitmqctl set_permissions -p geijer elias ".*" ".*" ".*"', shell=True)