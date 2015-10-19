import os, sys, glob, celery, subprocess, swiftclient.client
from celery import group
from tasks import airfoil
from createslaves import create_slaves

def calc_n_workers(n_angles, max_task_per_worker):
	n = n_angles / max_task_per_worker
	if (n_angles % max_task_per_worker) != 0:
		n += 1
	return n

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

def start(an_start, an_stop, an_angles):
    angle_start = an_start
    angle_stop = an_stop
    n_angles = an_angles
    angle_diff = (angle_stop-angle_start)/n_angles

    #n_workers = calc_n_workers(n_angles, 4)

    master_key_pub_path = '/etc/ssh/ssh_host_rsa_key.pub'
    master_key_path = '/etc/ssh/ssh_host_rsa_key'
    master_ip = subprocess.check_output("wget -qO- http://ipecho.net/plain ; echo", shell=True).rstrip()

    substitute('    - export master_ip="' + master_ip +'"', 'export master_ip=', 'userdata-slave.yml')

    slave_list = create_slaves(n_angles)

    #job = group([airfoil(n*angle_diff) for n in range(1, n_angles)])
    #result = job.apply_async()
    return slave_list