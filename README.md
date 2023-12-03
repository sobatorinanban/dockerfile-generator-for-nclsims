# dockerfile-generator-for-nclsims
[W.I.P.] Dockerfile generator for simulator made by NCL (e.g. ncl_sfcsim) in repeated experiments.  

This program generates a Dockerfile for repeated experimentation with the simulator made by NCL.  
I have not checked them all, but they probably work with most NCL simulators.  
Checked simulators: ncl_sfcsim, ncl_icn-sfcsim.

# How to use 
### about files
- dockerfile-generator.py
    - Main program
- ccnchanger.py
    - Used to vary CCN (Communication to Computation Ratio) in main program
- Dockerfile
    - Dockerfile template for nclsims
- crontab
    - Crontab configuration template for nclsims
- sim_autoexecutor.sh 
    - Script template for repeated experiments.

## Setting
Before executing the main program (dockerfile-generator.py), you can modify several template files.  
If you want to change how often the simulator runs (the default period is 20 min), do the following: edit `crontab` file with and editor. The newline code is LF.

## Use (Generating Dockerfiles)
Run dockerfile-generator.py by `python ./dockerfile-generator.py`.  
Then, follow the instructions to enter infomation for the configuration. At this time, if the simulator type is set to SFC, you can enter additional settings for CCR.