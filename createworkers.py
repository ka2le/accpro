import os, sys, subprocess
from novaclient.client import Client

# Replaces the line old in the file file with the new line new
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


# Crates n_workers workers with key_name as keypair and worker_prefix as prefix name of each worker.
# key_name and worker_prefix are enviroment variables set by userdata
def create_workers(n_workers):
    if not (0 <= n_workers <= 8):
        n_workers = 1

    worker_prefix = os.environ['worker_prefix']
    keyname = os.environ['key_name']

    config = {'username':os.environ['OS_USERNAME'],
        'api_key':os.environ['OS_PASSWORD'],
        'project_id':os.environ['OS_TENANT_NAME'],
        'auth_url':os.environ['OS_AUTH_URL']}

    nc = Client('2',**config)

    server_list = sorted(nc.servers.list(search_opts={'name': worker_prefix}), key=lambda w: w.name)
    n_workers_running = len(server_list)

    image = nc.images.find(id='59a19f79-f906-44e0-964a-22d66558cc54')
    flavor = nc.flavors.find(name='m1.medium')
    network = nc.networks.find(label='ACC-Course-net')
    keypair = nc.keypairs.find(name=keyname)

    # Get my ip
    master_ip = subprocess.check_output("wget -qO- http://ipecho.net/plain ; echo", shell=True).rstrip()
    
    # Set my ip as master_ip in the userdata that the workers use
    substitute('    - export master_ip="' + master_ip +'"', 'export master_ip=', 'userdata-worker.yml')

    
    with open('userdata-worker.yml', 'r') as ud:
        userdata = ud.read()

    for n in range(n_workers_running, n_workers_running + n_workers):
        worker_id = worker_prefix + str(n)
        try:
            server = nc.servers.create(name=worker_id, image=image, flavor=flavor.id, network=network.id,
                                        key_name=keypair.name, userdata=userdata, security_groups=None)
            server_list.append(server)
        finally:
            print "Creating " + worker_id + ' was successful!'

    return server_list


