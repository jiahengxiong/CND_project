import math

from matplotlib import pyplot as plt

from CND_project.tools.grooming.network import *
from CND_project.tools.no_grooming.ZR import gen_request
from CND_project.tools.grooming.ZR_opaque import gene_auxiliary_graph, update_weight, serve_request


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


if __name__ == '__main__':
    ZR_opaque = network()
    G = ZR_opaque.topology

    ini_num_request = 350
    requests = gen_request(ini_num_request)
    traffic = 0
    ZR_opaque_serve(ZR_opaque, requests)
