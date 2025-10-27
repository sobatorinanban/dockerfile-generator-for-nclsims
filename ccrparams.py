import math
import numpy as np

# application parameters
vnf_workload_min = 3000
vnf_workload_max = 10000

# environment parameters
node_bandwidth_min = 100
node_bandwidth_max = 1000
node_mips_min = 2000
node_mips_max = 4000

def generate_ccr_params_fixed_time(
    num_plots: int, 
    min_ccr: float = 0.1, 
    max_ccr: float = 10.0, 
    base_workload_min: float = float(vnf_workload_min), 
    base_workload_max: float = float(vnf_workload_max),
    base_ccr_for_time: float = 0.1) -> (list, float):
    # Generate CCR parameters for the required number of plots
    # with keeping the total application exexution time unchanged.

    node_bandwidth_median = (node_bandwidth_min + node_bandwidth_max) / 2
    node_mips_median = (node_mips_min + node_mips_max) /2

    # 1. Calculate the baseline value
    ## The average value and distribution ratio of the baseline Workload
    average_workload_base = (base_workload_min + base_workload_max) / 2.0
    workload_half_spread_base = base_workload_max - average_workload_base
    
    if average_workload_base > 0:
        spread_ratio = workload_half_spread_base / average_workload_base
    else:
        spread_ratio = 0.0

    ## The baseline of computation time
    time_comp_base = average_workload_base / node_mips_median
    ## The baseline of communication time (CCR=0.1)
    time_comm_base = time_comp_base * base_ccr_for_time
    
    ## The target of application execution time 
    T_target = time_comp_base + time_comm_base

    # 2. Generate plots of CCR
    target_ccr_values = np.linspace(min_ccr, max_ccr, num_plots+1)
    param_list = []
    
    # 3. Generate parameters for each CCR
    for ccr in target_ccr_values:
        
        ## Calculate computation time and communication time that satisfy target time
        time_comp_new = T_target / (1.0 + ccr)
        time_comm_new = (T_target * ccr) / (1.0 + ccr)
        
        ## Calculate the new average Workload and average Datasize
        average_workload_new = time_comp_new * node_mips_median
        average_datasize_new = time_comm_new * node_bandwidth_median
        
        ## Calculate each min/max value by applying the baseline distribution ratio
        workload_half_spread = average_workload_new * spread_ratio
        workload_min = max(0.0, average_workload_new - workload_half_spread)
        workload_max = average_workload_new + workload_half_spread
        
        datasize_half_spread = average_datasize_new * spread_ratio
        datasize_min = max(0.0, average_datasize_new - datasize_half_spread)
        datasize_max = average_datasize_new + datasize_half_spread

        workload_min = max(1, int(round(workload_min)))
        workload_max = max(1, int(round(workload_max)))
        datasize_min = max(1, int(round(datasize_min)))
        datasize_max = max(1, int(round(datasize_max)))
        if workload_max < workload_min:
            workload_min, workload_max = workload_max, workload_min
        if datasize_max < datasize_min:
            datasize_min, datasize_max = datasize_max, datasize_min
        
        param_list.append((datasize_min, datasize_max, workload_min, workload_max))
        
    return param_list, T_target

def generate_ccr_params(plot_num):
    ccr_interval = 10 / plot_num
    # varied_vnf_datasize = [[1, 100, -1, -1], [], ...]
    varied_vnf_datasize = []
    median_vnf_workload = (vnf_workload_min + vnf_workload_max) / 2

    median_node_bandwidth = (100 + 1000) / 2
    median_node_mips = (2000 + 4000) / 2

    ccr = 0
    for i in range(0, plot_num+1):
        vnf_datasize_min = 0
        vnf_datasize_max = 0
        median_vnf_datasize = 0
        if(i == 0):
            median_vnf_datasize = math.floor((0.1 * median_node_bandwidth * median_vnf_workload) / median_node_mips)
            # vnf_datasize_min = math.floor(median_vnf_datasize / 2)
            # vnf_datasize_max = math.floor(median_vnf_datasize + (median_vnf_datasize / 2))
            vnf_datasize_min = 1
            vnf_datasize_max = 10
        elif(i == plot_num):
            median_vnf_datasize = math.floor((10.0 * median_node_bandwidth * median_vnf_workload) / median_node_mips)
            vnf_datasize_min = math.floor(median_vnf_datasize / 2)
            vnf_datasize_max = math.floor(median_vnf_datasize + (median_vnf_datasize / 2))
        else:
            ccr += ccr_interval
            # print('plot' + str(i) +"'s CCR: " + str(ccr))
            median_vnf_datasize = math.floor((ccr * median_node_bandwidth * median_vnf_workload) / median_node_mips)
            vnf_datasize_min = math.floor(median_vnf_datasize / 2)
            vnf_datasize_max = math.floor(median_vnf_datasize + (median_vnf_datasize / 2))

        varied_vnf_datasize.append((vnf_datasize_min, vnf_datasize_max, -1, -1))

    return varied_vnf_datasize