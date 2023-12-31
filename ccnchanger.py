import math

vnf_weight_min = 3000
vnf_weight_max = 10000
node_bandwidth_min = 100
node_bandwidth_max = 1000
node_mips_min = 2000
node_mips_max = 4000

def ccn_chaner(plot_num):
    ccr_interval = 10 / plot_num
    # median_vnf_datasize = [[50, 1, 100], [], ...]
    varied_vnf_datasize = []
    median_vnf_workload = (vnf_weight_min + vnf_weight_max) / 2

    median_node_bandwidth = (100 + 1000) / 2
    median_node_mips = (2000 + 4000) / 2

    ccr = 0
    for i in range(0, plot_num+1):
        vnf_datasize_min = 0
        vnf_datasize_max = 0
        median_vnf_datasize = 0
        if(i == 0):
            median_vnf_datasize = math.floor((0.1 * median_node_bandwidth * median_vnf_workload) / median_node_mips)
            vnf_datasize_min = math.floor(median_vnf_datasize / 2)
            vnf_datasize_max = math.floor(median_vnf_datasize + (median_vnf_datasize / 2))
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

        varied_vnf_datasize.append([median_vnf_datasize, vnf_datasize_min, vnf_datasize_max])

    return varied_vnf_datasize