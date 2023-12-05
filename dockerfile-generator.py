import os 
import shutil
import sys 
import ccnchanger


## initialization
ccr_varied = False
interst_order_changed = False
is_nfs_mounted = False
interest_order_type = 'random'
varied_ccr = []
container_num = 1


print('--- Dockerfile generator for nclsims ---')
print('')


simulator = input('Which Simulator do you use? (e.g. repository name, like ncl_sfcsim): ')

run_sh = input('Which is the executable file of the simulator? (e.g. nfvrun.sh): ')

backup_dir = input("In which directory in the container do you want to back up the simulator logs? (e.g. /simulatorlog): ")

backup_with_nfs = input("Do you want to use NFS as a backup location for logs? (y/n): ")
if(backup_with_nfs == 'y'):
    print("Notice: You will need to manually edit the volumes paragraph in docker-compose.yml later to mount the NFS storage.")
    is_nfs_mounted = True

configfile = input('Which config file do you use (e.g. nfv.properties): ')
print("Notice: If you have not already placed the config file, please place it directly in the program's folder. ")

if(simulator == 'ncl_icn-sfcsim'):
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

    if(ccr_varied == False):
        container_num = int(input('Number of containers: '))
else:
    container_num = int(input('Number of containers: '))


## check and make export dir
foldername = input('Export folder name: ')
exportbasedir = './' + foldername + '/'
if not os.path.isdir(exportbasedir):
    os.makedirs(exportbasedir)

# checking if yml already touched
is_yml_touched = False
is_yml = os.path.isfile('./docker-compose.yml')
if is_yml:
    with open('./docker-compose.yml', mode='r', encoding='utf-8') as yml:
        for i, line in enumerate(yml):
            if 'services: ' in line:
                is_yml_touched = True
                break

if not (is_yml_touched):
    with open('./docker-compose.yml', mode='a', encoding='utf-8') as yml:
        yml.write('services: \n')
else:
    volumes_linenum = 0
    is_volumes_set = False
    with open('./docker-compose.yml', mode='r', encoding='utf-8') as yml:
        for num, line in enumerate(yml):
            if line == 'volumes: \n':
                volumes_linenum = num
                is_volumes_set = True
                break
    if(is_volumes_set):
        with open('./docker-compose.yml', mode='r+', encoding='utf-8') as yml:
            lines = yml.readlines()
            yml.seek(0)
            yml.truncate()
            for num, line in enumerate(lines):
                if num < volumes_linenum:
                    yml.write(line)


for i in range(0, container_num):
    folderdir = exportbasedir + str(i) + '/'
    if(ccr_varied):
        folderdir = exportbasedir + 'ccrplot' + str(i) + '/'
        if(interst_order_changed):
            folderdir = exportbasedir + interest_order_type + '/' + 'ccrplot' + str(i) + '/'
    else:
        if(interst_order_changed):
            folderdir = exportbasedir + interest_order_type + '/' + str(i) + '/'
    if not os.path.isdir(folderdir):
        os.makedirs(folderdir)

    config_type = str(i)
    if(ccr_varied):
        config_type = 'ccrplot' + str(i)
        if(interst_order_changed):
            config_type = interest_order_type + "/" + 'ccrplot' + str(i)
    else:
        if(interst_order_changed):
            config_type = interest_order_type + "/" + str(i)

    shutil.copy2(configfile, folderdir)
    shutil.copy2("./sim_autoexecutor.sh", folderdir)
    shutil.copy2("./crontab", folderdir)
    shutil.copy2("./Dockerfile", folderdir)

    # Dockerfile
    with open(folderdir + 'Dockerfile', mode='r', encoding='utf-8') as reader:
        data_lines_dk = reader.read()
    data_lines_dk = data_lines_dk.replace('ENV SIMULATOR_NAME ncl_icn-sfcsim', 'ENV SIMULATOR_NAME ' + simulator)
    data_lines_dk = data_lines_dk.replace('ENV LOGBACKUP_DIR /simulator-logs', 'ENV LOGBACKUP_DIR ' + backup_dir)
    data_lines_dk = data_lines_dk.replace('ENV CONFIG_TYPE random/0', 'ENV CONFIG_TYPE ' + config_type)
    data_lines_dk = data_lines_dk.replace('ENV RUN_SH = nfvrun.sh', 'ENV RUN_SH = ' + run_sh)
    with open(folderdir + 'Dockerfile', mode='w', encoding='utf-8') as writer:
        writer.write(data_lines_dk)

    # Shellscript (sim_autoexecutor.sh)
    with open(folderdir + 'sim_autoexecutor.sh', mode='r', encoding='utf-8') as reader:
        data_lines_sh = reader.read()
    data_lines_sh = data_lines_sh.replace('BACKUPDIR="/test-sim-log"', 'BACKUPDIR=' + '"' + backup_dir + '/' + config_type + '"')
    data_lines_sh = data_lines_sh.replace('SIMDIR="/simulator/ncl_icn-sfcsim"', 'SIMDIR="/simulator/' + simulator + '"')
    data_lines_sh = data_lines_sh.replace('LOGDIR="/simulator/ncl_icn-sfcsim/is"', 'LOGDIR="/simulator/' + '"' + simulator + '/is"')
    data_lines_sh = data_lines_sh.replace('RUNSH="./nfvrun.sh"', 'RUNSH="./' + run_sh + '"')
    with open(folderdir + 'sim_autoexecutor.sh', mode='w', encoding='utf-8') as writer:
        writer.write(data_lines_sh)

    # .properties
    with open(folderdir + configfile, mode='r', encoding='utf-8') as reader:
        data_lines_pr = reader.read()
    if(ccr_varied):
        data_lines_pr = data_lines_pr.replace('vnf_datasize_min=1', 'vnf_datasize_min=' + str(varied_ccr[i][1]))
        data_lines_pr = data_lines_pr.replace('vnf_datasize_max=1000', 'vnf_datasize_max=' +str(varied_ccr[i][2]))
        print('plot' + str(i) + "'s Average Datasize of VNF: " + str(varied_ccr[i][0]))
    if(interst_order_changed):
        mode = 0
        if(interest_order_type == 'random'):
            mode = 0
        elif(interest_order_type == 'workload'):
            mode = 1
        elif(interest_order_type == 'blevel'):
            mode = 2
        data_lines_pr = data_lines_pr.replace('sfc_vnf_ordering_mode=0', 'sfc_vnf_ordering_mode=' + str(mode))
    with open(folderdir + configfile, mode='w', encoding='utf-8') as writer:
        writer.write(data_lines_pr)

    # docker-compose.yml -- services
    with open('./docker-compose.yml', mode='a', encoding='utf-8') as yml:
        yml.write('  ' + config_type + ": " + '\n')
        yml.write('    ' + 'build: ' + folderdir + '\n')
        if(is_nfs_mounted):    
            yml.write('    ' + 'volumes: \n' )
            yml.write('      ' + '- log_backup:' + backup_dir + '\n')
        yml.write('\n')


# docker-compose.yml -- volumes
if(is_nfs_mounted):
    with open('./docker-compose.yml', mode='a', encoding='utf-8') as yml:
        yml.write('volumes: \n')
        yml.write('  ' + 'log_backup: \n')
        yml.write('    ' + 'driver_opts: \n')
        yml.write('      ' + 'type: nfs \n')
        yml.write('      ' + 'o: "addr=" \n')
        yml.write('      ' + 'device: "" \n')


print('')    
print('--- Dockerfile and docker-compose.yml exported ---')