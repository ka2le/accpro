import os, sys, glob, celery, subprocess, swiftclient.client
from celery import group
from tasks import airfoil
from createslaves import create_slaves

def calc_n_workers(n_angles, max_task_per_worker):
	n = n_angles / max_task_per_worker
	if (n_angles % max_task_per_worker) != 0:
		n += 1
	return n

def start(angle_start, angle_stop, n_angles):
    angle_diff = (angle_stop-angle_start)/n_angles
    #n_workers = calc_n_workers(n_angles, 2)
    slave_list = create_slaves(n_angles)

    #job = group([airfoil.s(n*angle_diff) for n in range(1, n_angles+1)])
    #result = job.apply_async()

    return slave_list