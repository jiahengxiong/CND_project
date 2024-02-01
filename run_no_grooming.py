import networkx as nx
from utils.network import network as N
import random
from utils.utils import *
import matplotlib.pyplot as plt
import heapq




def ZR_serve(network, requests):
    request_table = []
    for i in requests:
        shortest_path = find_shortest_path(i, network)
        print(shortest_path)


if __name__ == '__main__':
    ZR = N()
    ZR_OEO = N()
    OEO = N()
    ZR.get_topology()
    ZR_OEO.get_topology()
    OEO.get_topology()

    init_num_request = 1
    request_list = gen_request(init_num_request)
    request_list = [(2,3,400,1)]

    ZR_serve(ZR, request_list)
