import os 
import sys 
import ccnchanger

simulator = 'default'

print('--- Dockerfile generator for simulator ---')

if(len(sys.argv) <= 1):
    simulator = str(sys.argv[1])
    print('Simulator type has been set: simulator')

sim_source = input('Source of simulator (e.g. GitHub, etc): ')
sim_dir = input('Base directory to install simulator: ')
configfile_dir = input('Relative path of config file: ')
container_nmm = input('Number of containers: ')

if(simulator == 'sfcsim' or simulator == 'icn-sfcsim'):
    is_ccn_changing = input('Do you want to experiment with varing CCN? (y/n) :')
    if(is_ccn_changing == 'y'):


