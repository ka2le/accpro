import os
import time
from novaclient.client import Client

def create_slaves(n_workers):
    config = {'username':os.environ['OS_USERNAME'],
        'api_key':os.environ['OS_PASSWORD'],
        'project_id':os.environ['OS_TENANT_NAME'],
        'auth_url':os.environ['OS_AUTH_URL']}

    nc = Client('2',**config)

    server_list = []

    master_key_pub_path = '/etc/ssh/ssh_host_rsa_key.pub'
    master_key_path = '/etc/ssh/ssh_host_rsa_key'

    # Clear all the old worker keypairs
    for k in nc.keypairs.findall():
        if (k.id != 'lundekey'):
            nc.keypairs.delete(k)

    image = nc.images.find(id='59a19f79-f906-44e0-964a-22d66558cc54')
    flavor = nc.flavors.find(name='m1.medium')
    network = nc.networks.find(label='ACC-Course-net')
    userdata = open('userdata-slave.yml', 'r')

    with open(os.path.expanduser(master_key_pub_path)) as fpubkey:
        pubkey = fpubkey.read()
        for n in range(0, n_workers):
            worker_id = 'lundestance' + str(n)
            worker_key_id = 'lundekey' + str(n)
            if not nc.keypairs.findall(name=worker_id):
                nc.keypairs.create(name=worker_key_id, public_key=pubkey)
            try:
                server = nc.servers.create(name=worker_id, image=image, flavor=flavor.id, network=network.id,
                                            key_name=worker_key_id, userdata=userdata, security_groups=None)
                print dir(server)
                server_list.append(server)
            finally:
                print "Creating " + worker_id + ' was successful!'
        
        for server in server_list:
            floating_ips = nc.floating_ips.list()
            state = server.status
            while(state == 'BUILD'):
                time.sleep(4)
                server = nc.servers.get(server.id)
                state = server.status

            for ip in floating_ips:
                if ip.instance_id == None:
                    server.add_floating_ip(ip)
                    print '%s with ip: %s' % (server.name, str(ip.ip))
                    break
            else:
                print 'No available floating IPs in the pool'

    return str(server_list)


