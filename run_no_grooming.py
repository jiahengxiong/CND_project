import networkx as nx
from utils.network import network as N
from utils.utils import *
import matplotlib.pyplot as plt
import heapq
import math


def ZR_serve(network, requests):
    request_table = {}
    G = network.topology
    num_served = 0
    cost = 0
    for i in requests:
        path, modulation = find_shortest_path(i, network)
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
    average_cost = cost/num_served
    print(average_cost)


def gen_request(num):
    rate_list = [100, 200, 300, 400]
    request = []
    for i in range(0, num):
        src, dst = random.sample(range(1, 8), 2)
        rate = random.sample(range(0, 3), 1)[0]

        request.append((src, dst, rate_list[rate], i + 1))

    return request


if __name__ == '__main__':
    ZR = N()
    ZR_OEO = N()
    OEO = N()
    ZR.get_topology()
    ZR_OEO.get_topology()
    OEO.get_topology()

    init_num_request = 100
    request_list = gen_request(init_num_request)
    print(request_list)

    ZR_serve(ZR, request_list)
