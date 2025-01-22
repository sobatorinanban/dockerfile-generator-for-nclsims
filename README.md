# dockerfile-generator-for-nclsims
Dockerfile generator for repeated experiments on NCL simulators (e.g. ncl_sfcsim).

This program generates a Dockerfile for repeated experimentation with the simulator made by NCL.  
I have not checked them all, but they probably work with most NCL simulators.  
Checked simulators: ncl_sfcsim, ncl_icn-sfcsim.

# How to use 
### About files
- dockerfile-generator.py
    - **Main program**
- ccnchanger.py
    - Used to vary CCN (Communication to Computation Ratio) in main program
- Dockerfile
    - Dockerfile template for nclsims
- Dockerfile.builder
    - Dockerfile template for building nclsims
- crontab
    - Crontab template for nclsims
- sim_autoexecutor.sh 
    - Script template for repeated experiments

### Required dependencies
- python3
- pyyaml

## Setting
Before running the main program, a configuration file (such as `xxx.properties`) must be placed directly in the same location as the main program.  
You can modify several template files (Dockerfile, sim_autoexecutor.sh, etc) if you want to.  
If you want to change how often the simulator runs (the default period is 20 min), do the following: edit `crontab` file with and editor. Only LF is allowed as a line feed code.  

## Use (Generating Dockerfiles)
Run main program by `python ./dockerfile-generator.py`.  
Then, follow the instructions to enter infomation for the configuration.  
If the simulator type is set to ncl_sfcsim, you can enter additional settings for CCR. 

## Example
Place configration file (In my case, `auto.properties`) in the same directory as `dockerfile-generator.py`.  

Run `python ./dockerfile-generator.py`.  
```
--- Dockerfile generator for nclsims ---

Which Simulator do you use? (e.g. repository name, like ncl_sfcsim): ncl_icn-sfcsim
Which is the executable file of the simulator? (e.g. nfvrun.sh): automain.sh    
In which directory in the container do you want to back up the simulator logs? (e.g. /simulatorlog): /simulator-log
Do you want to use NFS as a backup location for logs? (y/n): y
Notice: You will need to manually edit the volumes paragraph in docker-compose.yml later to mount the NFS storage.
Which config file do you use (e.g. nfv.properties): auto.properties
Notice: If you have not already placed the config file, please place it directly in the program's folder.
Do you want to experiment with varing CCN? (y/n): y
Number of CCR plots: 10
Do you want to change the interest sending order? (y/n):y
Which type of Interest sending order (random, workload, or blevel): workload
Export folder name: exp-workload
plot0's Average Datasize of VNF: 50
plot1's Average Datasize of VNF: 1191
plot2's Average Datasize of VNF: 2383
plot3's Average Datasize of VNF: 3575
plot4's Average Datasize of VNF: 4766
plot5's Average Datasize of VNF: 5958
plot6's Average Datasize of VNF: 7150
plot7's Average Datasize of VNF: 8341
plot8's Average Datasize of VNF: 9533
plot9's Average Datasize of VNF: 10725
plot10's Average Datasize of VNF: 11916

--- Dockerfile and docker-compose.yml exported ---
```
Open docker-compose.yml by `vi docker-compose.yml`.  

Edit `volumes: `paragraph in `docker-compose.yml` to configure NFS storage.  

Step1

Run `docker compose run builder`.  Clone and build simulator.

Step2

Run `docker compose up`.  Running simulator.
