import math

from matplotlib import pyplot as plt

from CND_project.tools.grooming.network import *
from CND_project.tools.no_grooming.ZR import gen_request
from CND_project.tools.grooming.ZR_opaque import gene_auxiliary_graph, update_weight, serve_request
from CND_project.tools.grooming.ZR_bypass import gene_auxiliary_graph_ZR_bypass, update_weight_ZR_bypass, reserve_path, serve_request_ZR_bypass

def ZR_opaque_serve(ZR_network, ZR_requests):
    G = ZR_network.topology
    cost = 0
    traffic = 0
    num_served = 0
    for request in ZR_requests:
        AG = gene_auxiliary_graph(G, request)
        AG = update_weight(AG)

        if nx.has_path(AG, source=request[0], target=request[1]):
            path = nx.dijkstra_path(AG, source=request[0], target=request[1])
            power = serve_request(G, path, request)
            cost += power
            traffic += request[2]*0.001
            num_served += 1

    print(cost / traffic, traffic, num_served, len(ZR_requests))


def ZR_bypass_serve(ZR_bypass_network, ZR_bypass_requests):
    G = ZR_bypass_network.topology
    cost = 0
    traffic = 0
    num_served = 0
    for request in ZR_bypass_requests:
        AG = gene_auxiliary_graph_ZR_bypass(G, request)
        AG = update_weight_ZR_bypass(AG)
        if nx.has_path(AG, source=request[0], target=request[1]):
            path = nx.dijkstra_path(AG, source=request[0], target=request[1])
            res_path = reserve_path(AG, path, request[2])
            #print(request, path, res_path)
            power = serve_request_ZR_bypass(G, path, request, res_path)
            cost += power
            traffic += request[2] * 0.001
            num_served += 1

    print(cost / traffic, traffic, num_served, len(ZR_bypass_requests))


if __name__ == '__main__':
    ZR_opaque = network()
    ZR_bypass = network()

    ini_num_request = 700
    requests = gen_request(ini_num_request)
    traffic = 0
    #ZR_opaque_serve(ZR_opaque, requests)
    ZR_bypass_serve(ZR_bypass, requests)
