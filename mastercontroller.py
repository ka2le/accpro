import os, sys, glob, celery, subprocess, swiftclient.client
from celery import group
from tasks import airfoil
from createslaves import create_slaves



def start(angle_start, angle_stop, n_angles):
    angle_diff = (angle_stop-angle_start)/n_angles
    n_workers = calc_n_workers(n_angles, 1)
    slave_list = create_slaves(n_workers)

    