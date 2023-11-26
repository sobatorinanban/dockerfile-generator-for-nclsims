import math

vnf_weight_min = 3000
vnf_weight_max = 10000
node_bandwidth_min = 100
node_bandwidth_max = 1000
node_mips_min = 2000
node_mips_max = 4000

def ccn_chaner(plot_num):
    ccn_interval = 10 / plot_num
    # median_vnf_datasize = [[0, 1000],[1.18, 2750], ...]
    median_vnf_datasize = []
    median_vnf_workload = (vnf_weight_min + vnf_weight_max) / 2

    median_node_bandwidth = (100 + 1000) / 2
    median_node_mips = (2000 + 4000) / 2

    for i in range(0, plot_num+1):
        datasize = 1
        actual_ccn = 0.1



        median_vnf_datasize.append([actual_ccn, datasize])

    return median_vnf_datasize