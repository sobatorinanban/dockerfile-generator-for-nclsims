import os
import shutil
import ccnchanger
import yaml


## initialization
ccr_varied = False
interest_order_changed = False
interest_sending_in_onestroke = False
sfc_vnf_num_varied = False
is_nfs_mounted = False
is_bind_mounted = False
bind_mount_dir = ''
interest_order_type = 'random'
varied_ccr = []
container_num = 1
max_vnf_num = 20
min_vnf_num = 20


print('--- Dockerfile generator for nclsims ---')
print('')


simulator = input('Which Simulator do you use? (e.g. repository name, like ncl_sfcsim): ')

simulator_branch = input('Which branch of Simulator do you use? (e.g. master): ')

run_sh = input('Which run-script file of the simulator do you use? (e.g. nfvrun.sh): ')

backup_dir = input("In which directory in the container do you want to back up the simulator logs? (e.g. /simulatorlog): ")

backup_with_nfs = input("Do you want to use NFS as a backup location for logs? (y/n): ")
if(backup_with_nfs == 'y'):
    print("    Notice: You will need to manually edit the volumes paragraph in docker-compose.yml later to mount the NFS storage.")
    is_nfs_mounted = True
elif(backup_with_nfs == 'n'):
    backup_with_bind_mounting = input('Do you want to use Bind Mounting as a backup location for logs? (y/n): ')
    if(backup_with_bind_mounting == 'y'):
        print("    Notice: You will need to manually prepare a directory for Bind Mounting on the Docker host.")
        bind_mount_dir = input('In which directory on the Docker host do you want to use as a Bind Mounting dir? (e.g. ./bind-mounting): ')
        is_bind_mounted = True

configfile = input('Which config file do you use (e.g. nfv.properties): ')
print("    Notice: If you have not already placed the config file, please place it directly in the program's folder. ")

if(simulator == 'ncl_icn-sfcsim'):
    ### ncl_icn-sfcsim section
    is_vnf_num_changing = input('Do you want to experiment with varing VNF nums? (y/n): ')
    if(is_vnf_num_changing == 'y'):
        sfc_vnf_num_varied = True
        max_vnf_num = int(input('Maximum number of VNFs in SFC: '))
        min_vnf_num = int(input('Minimum number of VNFs in SFC: '))

        # check and fix misstake
        if(min_vnf_num > max_vnf_num):
            tmp = max_vnf_num
            max_vnf_num = min_vnf_num
            min_vnf_num = tmp

    else:
        sfc_vnf_num_varied = False
        max_vnf_num = 20
        min_vnf_num = 20

    is_ccn_changing = input('Do you want to experiment with varing CCN? (y/n): ')
    if(is_ccn_changing == 'y'):
        ccr_plotnum = int(input('Number of CCR plots: '))
        varied_ccr = ccnchanger.ccn_chaner(int(ccr_plotnum))
        ccr_varied = True
        container_num = ccr_plotnum + 1

    if(simulator == 'ncl_icn-sfcsim' or simulator == 'icn-sfcsim'):
        is_change_interest_sending_method = input('Do you want to change the interest sending method to one-stroke(unicast)? (y/n): ')
        if(is_change_interest_sending_method == 'y'):
            interest_sending_in_onestroke = True

        is_change_interest_order = input('Do you want to change the interest sending order? (y/n):')
        if(is_change_interest_order == 'y'):
            interest_order_changed = True
            interest_order_type = input('Which type of Interest sending order (random, workload, or blevel): ')

    if(ccr_varied == False):
        container_num = int(input('Number of containers: '))
else:
    ### other simulator (default) section
    container_num = int(input('Number of containers: '))


## check and make export dir
foldername = input('Export folder name: ')
exportbasedir = './' + foldername + '/'
if not os.path.isdir(exportbasedir):
    os.makedirs(exportbasedir)

# make docker-compose.yml builder section
yaml_data = {
    'version': '3.8',
    'services': {
        'builder': {
            'build': {
                'context': '.',
                'dockerfile': 'Dockerfile.builder',
            },
            'image': 'ncl-javaimg:latest',
            'container_name': 'builder',
            'working_dir': '/app',
            'volumes': [
                f'./{foldername}/sims:/app'
            ],
            'command': f'bash -c "if [ -d {simulator} ]; then cd {simulator} && git checkout {simulator_branch} && ant build; else git clone https://github.com/ncl-teu/{simulator}.git && cd {simulator} && git checkout {simulator_branch} && ant build; fi"'
        },
    }
}

# nvf roop
for vnfnum in range(min_vnf_num, max_vnf_num+1, 5):


    for i in range(0, container_num):
        config_type = ""
        if(ccr_varied):
            config_type += 'ccrplot' + str(i)
        else:
            config_type += str(i)
        if(sfc_vnf_num_varied):
            config_type = str(vnfnum) + 'vnfs' + "/" + config_type
        if(interest_sending_in_onestroke):
            config_type = "in-one-stroke" + "/" + config_type
        if(interest_order_changed):
            config_type = interest_order_type + "/" + config_type

        folderdir = exportbasedir + config_type + "/"
        if not os.path.isdir(folderdir):
            os.makedirs(folderdir)



        shutil.copy2(configfile, folderdir)
        shutil.copy2("./sim_autoexecutor.sh", folderdir)
        shutil.copy2("./crontab", folderdir)
        shutil.copy2("./Dockerfile", exportbasedir) # 配置を1つ上の階層へ

        with open(folderdir + 'sim_autoexecutor.sh', mode='r', encoding='utf-8') as reader:
            data_lines_sh = reader.read()
        data_lines_sh = data_lines_sh.replace('BACKUPDIR="/default-sim-log"', 'BACKUPDIR=' + '"' + backup_dir + '/' + config_type + '"')
        data_lines_sh = data_lines_sh.replace('RUNSH="./default.sh"', 'RUNSH="./' + run_sh + '"')
        with open(folderdir + 'sim_autoexecutor.sh', mode='w', encoding='utf-8', newline='\n') as writer:
            writer.write(data_lines_sh)

        # .properties
        with open(folderdir + configfile, mode='r', encoding='utf-8') as reader:
            data_lines_pr = reader.read()
        if(ccr_varied):
            data_lines_pr = data_lines_pr.replace('sfc_vnf_num=20', 'sfc_vnf_num=' + str(vnfnum))
            data_lines_pr = data_lines_pr.replace('sfc_vnf_num_min=20', 'sfc_vnf_num_min=' + str(vnfnum))
            data_lines_pr = data_lines_pr.replace('sfc_vnf_num_max=20', 'sfc_vnf_num_max=' + str(vnfnum))
        if(ccr_varied):
            data_lines_pr = data_lines_pr.replace('vnf_datasize_min=1', 'vnf_datasize_min=' + str(varied_ccr[i][1]))
            data_lines_pr = data_lines_pr.replace('vnf_datasize_max=1000', 'vnf_datasize_max=' +str(varied_ccr[i][2]))
            print('plot' + str(i) + "'s Average Datasize of VNF: " + str(varied_ccr[i][0]))
        if(interest_order_changed):
            mode = 0
            if(interest_order_type == 'random'):
                mode = 0
            elif(interest_order_type == 'workload'):
                mode = 1
            elif(interest_order_type == 'blevel'):
                mode = 2
            data_lines_pr = data_lines_pr.replace('sfc_vnf_ordering_mode=0', 'sfc_vnf_ordering_mode=' + str(mode))
        if(interest_sending_in_onestroke):
            data_lines_pr = data_lines_pr.replace('ccn_interests_sending_mode=0', 'ccn_interests_sending_mode=' + '1')
        with open(folderdir + configfile, mode='w', encoding='utf-8', newline='\n') as writer:
            writer.write(data_lines_pr)

        # make docker-compose.yml services section
        yaml_data['services'][config_type.replace('/', '')] = {
            'build': {
                'context': f'./{foldername}',
                'args': {
                    'CONFIG_TYPE': config_type,
                    'SIMULATOR_NAME': simulator,
                    'CONFIG_FILE': configfile,
                    'RUN_SH': run_sh,
                },
            },
            'depends_on': {
                'builder': {
                    'condition': 'service_completed_successfully'
                }
            },
            'volumes': [
                f'./{foldername}/sims:/app',
                f'{bind_mount_dir}:{backup_dir}'
            ]
        }

# write yml file(only over write)
with open("docker-compose.yml", 'w') as file:
    yaml.dump(yaml_data, file, default_flow_style=False, sort_keys=False)

# docker-compose.yml -- volumes
if(is_nfs_mounted):
    with open('./docker-compose.yml', mode='a', encoding='utf-8', newline='\n') as yml:
        yml.write('volumes: \n')
        yml.write('  ' + 'log_backup: \n')
        yml.write('    ' + 'driver_opts: \n')
        yml.write('      ' + 'type: nfs \n')
        yml.write('      ' + 'o: "addr=" \n')
        yml.write('      ' + 'device: "" \n')


print('')
print('--- Dockerfile and docker-compose.yml exported ---')