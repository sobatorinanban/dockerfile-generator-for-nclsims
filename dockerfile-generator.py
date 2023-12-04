import os 
import shutil
import sys 
import ccnchanger


## initialization
ccr_varied = False
interst_order_changed = False
interest_order_type = 'random'
varied_ccr = []
container_num = 1

print('--- Dockerfile generator for nclsims ---')

simulator = input('Which Simulator do you use? (e.g. repository name, like ncl_sfcsim): ')
backup_dir = input("In which directory in the container do you want to back up the simulator logs? (e.g. /simulatorlog): ")
configfile_dir = input('Which config file do you use (e.g. nfv.properties): ')
print("notice: If you have not already placed the config file, please place it directly in the program's folder. ")

if(simulator == 'sfcsim' or simulator == 'ncl_sfcsim' or simulator == 'icn-sfcsim' or simulator == 'ncl_icn-sfcsim'):
    is_ccn_changing = input('Do you want to experiment with varing CCN? (y/n): ')
    if(is_ccn_changing == 'y'):
        ccr_plotnum = int(input('Number of CCR plots: '))
        varied_ccr = ccnchanger.ccn_chaner(int(ccr_plotnum)) 
        ccr_varied = True
        container_num = ccr_plotnum + 1

    if(simulator == 'ncl_icn-sfcsim' or simulator == 'icn-sfcsim'):
        is_change_interest_order = input('Do you want to change the interest sending order? (y/n):')
        if(is_change_interest_order == 'y'):
            interst_order_changed = True
            interest_order_type = input('Which type of Interest sending order (random, workload, or blevel): ')
else:
    container_num = int(input('Number of containers: '))


## writing to dockerfile
foldername = input('Export folder name: ')
exportbasedir = './' + foldername + '/'
if not os.path.isdir(exportbasedir):
    os.makedirs(exportbasedir)

for i in range(0, container_num):
    folderdir = exportbasedir + str(i) + '/'
    if(ccr_varied):
        folderdir = exportbasedir + 'ccrplot' + str(i) + '/'
        if(interst_order_changed):
            folderdir = exportbasedir + interest_order_type + '/' + 'ccrplot' + str(i) + '/'
    if not os.path.isdir(folderdir):
        os.makedirs(folderdir)

    config_type = str(i)
    if(ccr_varied):
        config_type = 'ccrplot' + str(i)
        if(interst_order_changed):
            config_type = interest_order_type + "/" + 'ccrplot' + str(i)

    shutil.copy2(configfile_dir, folderdir)
    shutil.copy2("./sim_autoexecutor.sh", folderdir)
    shutil.copy2("./crontab", folderdir)
    shutil.copy2("./Dockerfile", folderdir)

    # Dockerfile
    with open(folderdir + 'Dockerfile', mode='r', encoding='utf-8') as reader:
        data_lines_dk = reader.read()
    data_lines_dk = data_lines_dk.replace("ENV SIMULATOR_NAME ncl_icn-sfcsim", "ENV SIMULATOR_NAME " + simulator)
    data_lines_dk = data_lines_dk.replace("ENV LOGBACKUP_DIR /simulator-logs", "ENV LOGBACKUP_DIR " + backup_dir)
    data_lines_dk = data_lines_dk.replace("ENV CONFIG_TYPE Random/0", "CONFIG_TYPE " + config_type)
    with open(folderdir + 'Dockerfile', mode='w', encoding='utf-8') as writer:
        writer.write(data_lines_dk)

    # Shellscript (sim_autoexecutor.sh)
    with open(folderdir + 'sim_autoexecutor.sh', mode='r', encoding='utf-8') as reader:
        data_lines_sh = reader.read()
    data_lines_sh = data_lines_sh.replace('BACKUPDIR="/test-sim-log"', 'BACKUPDIR=' + '"' + backup_dir + '/' + config_type + '"')
    data_lines_sh = data_lines_sh.replace('SIMDIR="/simulator/ncl_icn-sfcsim"', 'SIMDIR="/simulator/' + simulator + '"')
    data_lines_sh = data_lines_sh.replace('LOGDIR="/simulator/ncl_icn-sfcsim/is"', 'LOGDIR="/simulator/' + '"' + simulator + '/is"')
    with open(folderdir + 'sim_autoexecutor.sh', mode='w', encoding='utf-8') as writer:
        writer.write(data_lines_sh)


    


