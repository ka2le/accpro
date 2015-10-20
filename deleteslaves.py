import os
from novaclient.client import Client
 
config = {'username':os.environ['OS_USERNAME'],
          'api_key':os.environ['OS_PASSWORD'],
          'project_id':os.environ['OS_TENANT_NAME'],
          'auth_url':os.environ['OS_AUTH_URL'],
           }
 
nova = Client('2',**config)

instances = nova.servers.findall()
myid = "1205eee10f7c4aeebf180b3beb2ec60c"
for a in instances: 
    if a.user_id == myid:
    	if a.name != "lundestance-master":
        	a.delete()    