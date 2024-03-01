import json
import math
import time
from datetime import timedelta

import matplotlib.pyplot as plt

from CND_project.tools.no_grooming.OEO_bypass import *
from CND_project.tools.no_grooming.ZR_bypass import *
from CND_project.tools.no_grooming.ZR_opaque import gene_auxiliary_graph_ZR_opaque, update_weight_ZR_opaque, \
    serve_request_ZR_opaque
from CND_project.tools.no_grooming.network import *


def ZR_opaque_serve(ZR_opaque_network, ZR_requests):
    G = ZR_opaque_network.topology
    cost = 0
    traffic = 0
    num_served = 0
    for request in ZR_requests:
        AG = gene_auxiliary_graph_ZR_opaque(G, request)
        AG = update_weight_ZR_opaque(AG)
        if nx.has_path(AG, source=request[0], target=request[1]):
            path = nx.dijkstra_path(AG, source=request[0], target=request[1])
            power = serve_request_ZR_opaque(G, path, request)
            cost += power
            traffic += request[2] * 0.001
            num_served += 1

    print(cost / traffic, traffic, num_served, len(ZR_requests))
    return cost / traffic, traffic


def ZR_bypass_serve(ZR_bypass_network, ZR_bypass_requests):
    G = ZR_bypass_network.topology
    cost = 0
    traffic_served = 0
    num_served = 0
    for request in ZR_bypass_requests:
        AG = gene_auxiliary_graph_ZR_bypass(G, request)
        AG = update_weight_ZR_bypass(AG)
        if nx.has_path(AG, source=request[0], target=request[1]):
            path = nx.dijkstra_path(AG, source=request[0], target=request[1])
            res_path = reserve_path(AG, path, request[2])
            # print(request, path, res_path)
            power = serve_request_ZR_bypass(G, path, request, res_path)
            cost += power
            traffic_served += request[2] * 0.001
            num_served += 1

    print(cost / traffic_served, traffic_served, num_served, len(ZR_bypass_requests))
    return cost / traffic_served, traffic_served


def OEO_bypass_serve(OEO_bypass_network, OEO_bypass_requests):
    G = OEO_bypass_network.topology
    cost = 0
    traffic_served = 0
    num_served = 0
    for request in OEO_bypass_requests:
        AG = gene_auxiliary_graph_OEO_bypass(G, request)
        AG = update_weight_OEO_bypass(AG)
        if nx.has_path(AG, source=request[0], target=request[1]):
            path = nx.dijkstra_path(AG, source=request[0], target=request[1])
            res_path = reserve_path(AG, path, request[2])
            # print(request, path, res_path)
            power = serve_request_OEO_bypass(G, path, request, res_path)
            cost += power
            traffic_served += request[2] * 0.001
            num_served += 1

    print(cost / traffic_served, traffic_served, num_served, len(OEO_bypass_requests))
    return cost / traffic_served, traffic_served


if __name__ == '__main__':
    start_time = time.time()
    for i in range(0, 10):
        zr_bypass = {}
        zr_opaque = {}
        oeo_bypass = {}
        for init_num_request in [350, 400, 450, 500, 550, 600, 650, 700]:
            total_traffic = init_num_request * 0.001 * 250
            ZR_opaque = National_network()
            ZR_bypass = National_network()
            OEO_bypass = National_network()
            start_time = time.time()
            requests = gen_request(init_num_request)
            average_cost_ZR_opaque, served_traffic_ZR_opaque = ZR_opaque_serve(ZR_opaque, requests)
            average_cost_ZR_bypass, served_traffic_ZR_bypass = ZR_bypass_serve(ZR_bypass, requests)
            average_cost_OEO_bypass, served_traffic_OEO_bypass = OEO_bypass_serve(OEO_bypass, requests)
            zr_bypass[total_traffic] = {'average_cost': average_cost_ZR_bypass,
                                        'served_traffic': served_traffic_ZR_bypass}
            zr_opaque[total_traffic] = {'average_cost': average_cost_ZR_opaque,
                                        'served_traffic': served_traffic_ZR_opaque}
            oeo_bypass[total_traffic] = {'average_cost': average_cost_OEO_bypass,
                                         'served_traffic': served_traffic_OEO_bypass}
        with open('no_grooming.txt', 'a') as file:
            file.write("ZR_bypass:\n")
            file.write(json.dumps(zr_bypass) + '\n')
            file.write("ZR_opaque:\n")
            file.write(json.dumps(zr_opaque) + '\n')
            file.write("OEO_bypass:\n")
            file.write(json.dumps(oeo_bypass) + '\n')
            file.write("****************************\n")
    end_time = time.time()
    elapsed_time = end_time - start_time
    formatted_time = str(timedelta(seconds=elapsed_time))
    print("Total time:", formatted_time)