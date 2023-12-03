import os 
import sys 
import ccnchanger


## initialization
ccr_varied = False
varied_ccr = []

print('--- Dockerfile generator for nclsims ---')

simulator = input('Simulator type (e.g. ncl_sfcsim): ')
sim_dir = input('Base directory to install simulator: ')
configfile_dir = input('Relative path of config file (e.g. nfv.properties): ')
container_num = 1

if(simulator == 'sfcsim' or simulator == 'ncl_sfcsim' or simulator == 'icn-sfcsim' or simulator == 'ncl_icn-sfcsim'):
    is_ccn_changing = input('Do you want to experiment with varing CCN? (y/n): ')
    if(is_ccn_changing == 'y'):
        ccr_plotnum = int(input('Number of CCR plots: '))
        varied_ccr = ccnchanger.ccn_chaner(int(ccr_plotnum))
        ccr_varied = True
        container_num = varied_ccr + 1
        print('ccr5: ' + str(5))
        print('datasize min: ' + str(varied_ccr[5][1]))
        print('datasize min: ' + str(varied_ccr[5][2]))
else:
    container_num = int(input('Number of containers: '))


## writing to dockerfile
foldername = input('Export Dir: ')
exportdir = './' + foldername + '/'
if not os.path.isdir(exportdir):
    os.makedirs(exportdir)

for i in range(0, container_num):
    filedir = exportdir + 'nclsimdockerfile' + str(i) + '.dockerfile'
    with open(filedir, mode='w') as f:
        f.write('test\n')
        f.write('test2\n')
    f.close()
    


