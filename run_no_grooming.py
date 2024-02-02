import networkx as nx
from utils.network import network as N
import random
from utils.utils import *
import matplotlib.pyplot as plt
import heapq


def ZR_serve(network, requests):
    global distance_table, modulation
    request_table = {}
    G = network.topology
    num_served = 0
    cost = 0
    for i in requests:
        path, modulation = find_shortest_path(i, network)
        distance_table = build_distance(path, network)
        # sorted_modulation = collections.OrderedDict(sorted(modulation.items(), key=lambda item: item[1]['reach']))
        if len(path) > 0:
            for j in range(0, len(path) - 1):
                G[path[j]][path[j + 1]]['channels'] = G[path[j]][path[j + 1]]['channels'] - 2
                G[path[j]][path[j + 1]]['occupied_channel'] = G[path[j]][path[j + 1]]['occupied_channel'] + 2
                G[path[j]][path[j + 1]]['occupied_requests'].append(i)
            request_table[i] = path
            num_served = num_served + 1
    for num, r in enumerate(request_table):
        power = compute_cost_ZR(request_table[r], distance_table, modulation)


if __name__ == '__main__':
    ZR = N()
    ZR_OEO = N()
    OEO = N()
    ZR.get_topology()
    ZR_OEO.get_topology()
    OEO.get_topology()

    init_num_request = 1
    request_list = gen_request(init_num_request)

    ZR_serve(ZR, request_list)
