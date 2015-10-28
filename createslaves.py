import os, sys, subprocess
from novaclient.client import Client

def substitute(new, old, file):
    f = open(file, "r")
    lines = f.readlines()
    f.close()

    f = open(file, "w")
    for line in lines:
        if not old in line:
            f.write(line)
        else:
            f.write(new + '\n')
    f.close()

def create_slaves(n_workers):
    config = {'username':os.environ['OS_USERNAME'],
        'api_key':os.environ['OS_PASSWORD'],
        'project_id':os.environ['OS_TENANT_NAME'],
        'auth_url':os.environ['OS_AUTH_URL']}

    nc = Client('2',**config)

    server_list = sorted(nc.servers.list(search_opts={'name': 'lundestance-slave'}), key=lambda w: w.name)
    n_workers_running = len(server_list)

    image = nc.images.find(id='59a19f79-f906-44e0-964a-22d66558cc54')
    flavor = nc.flavors.find(name='m1.medium')
    network = nc.networks.find(label='ACC-Course-net')
    keypair = nc.keypairs.find(name='lundekey')
    master_ip = subprocess.check_output("wget -qO- http://ipecho.net/plain ; echo", shell=True).rstrip()
    substitute('    - export master_ip="' + master_ip +'"', 'export master_ip=', 'userdata-slave.yml')

    
    with open('userdata-slave.yml', 'r') as ud:
        userdata = ud.read()

    for n in range(n_workers_running, n_workers_running + n_workers):
        worker_id = 'lundestance-slave' + str(n)
        try:
            server = nc.servers.create(name=worker_id, image=image, flavor=flavor.id, network=network.id,
                                        key_name=keypair.name, userdata=userdata, security_groups=None)
            server_list.append(server)
        finally:
            print "Creating " + worker_id + ' was successful!'

    return server_list


