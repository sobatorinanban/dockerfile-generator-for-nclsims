import math

def ccn_chaner(vnf_weight_min, vnf_weight_max, plot_num):
    ccn_interval = 10 / plot_num


    # median_vnf_datasize = [[],]
    median_vnf_datasize = {}
    median_vnf_workload = (vnf_weight_max + vnf_weight_min) / 2

    median_node_bandwidth = (100 + 1000) / 2
    median_node_mips = (2000 + 4000) / 2


    