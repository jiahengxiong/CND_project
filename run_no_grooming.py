import networkx as nx
from tools.network import network as N
from tools.utils import *
from tools.OEO import *
import matplotlib.pyplot as plt
import heapq
import math


def ZR_serve(network, requests):
    request_table = {}
    G = network.topology
    num_served = 0
    cost = 0
    for i in requests:
        path, modulation = find_shortest_path_ZR(i, network)
        # sorted_modulation = collections.OrderedDict(sorted(modulation.items(), key=lambda item: item[1]['reach']))
        if len(path) > 0:
            for j in range(0, len(path) - 1):
                G[path[j]][path[j + 1]]['channels'] = G[path[j]][path[j + 1]]['channels'] - math.ceil(
                    modulation[list(modulation.keys())[0]]['channel'] / 50)
                G[path[j]][path[j + 1]]['occupied_channel'] = G[path[j]][path[j + 1]]['occupied_channel'] + math.ceil(
                    modulation[list(modulation.keys())[0]]['channel'] / 50)
                G[path[j]][path[j + 1]]['occupied_requests'].append(i)
            request_table[i] = path
            num_served = num_served + 1
            power = compute_cost_ZR(path, modulation, network)
            cost = cost + power
    average_cost = cost / num_served
    print(average_cost, num_served)


def OEO_serve(network, requests):
    request_table = {}
    G = network.topology
    num_served = 0
    cost = 0
    for i in requests:
        path, modulation = find_shortest_path_OEO(i, network)
        # sorted_modulation = collections.OrderedDict(sorted(modulation.items(), key=lambda item: item[1]['reach']))
        if len(path) > 0:
            # assign modulation

            power = OEO_serve_request(path, modulation, network)
            num_served+=1

    print(num_served)


if __name__ == '__main__':
    ZR = N()
    ZR_OEO = N()
    OEO = N()
    ZR.get_topology()
    ZR_OEO.get_topology()
    OEO.get_topology()

    init_num_request = 350
    request_list = gen_request(init_num_request)
    #request_list = [(1, 4, 300, 1)]

    #ZR_serve(ZR, request_list)
    OEO_serve(OEO, request_list)
    G = OEO.topology

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True)

    edge_labels = {(u, v): d['channels'] for u, v, d in G.edges(data=True)}

    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.show()
