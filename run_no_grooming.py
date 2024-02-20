from CND_project.tools.no_grooming.ZR_opaque import find_shortest_path_opaque, compute_cost_opaque
from CND_project.tools.no_grooming.network import network as N
from CND_project.tools.no_grooming.ZR import *
from CND_project.tools.no_grooming.OEO import *
import matplotlib.pyplot as plt
import math
import json


def ZR_serve(network, requests):
    request_table = {}
    G = network.topology
    num_served = 0
    cost = 0
    Tpb = 0
    for i in requests:
        path, modulation = find_shortest_path_ZR(i, network)
        # sorted_modulation = collections.OrderedDict(sorted(modulation.items(), key=lambda item: item[1]['reach']))
        if len(path) > 0:
            for j in range(0, len(path) - 1):
                G[path[j]][path[j + 1]]['channels'] = G[path[j]][path[j + 1]]['channels'] - math.ceil(
                    modulation[list(modulation.keys())[0]]['channel'] / 25)
                G[path[j]][path[j + 1]]['occupied_channel'] = G[path[j]][path[j + 1]]['occupied_channel'] + math.ceil(
                    modulation[list(modulation.keys())[0]]['channel'] / 25)
                G[path[j]][path[j + 1]]['occupied_requests'].append(i)
            request_table[i] = path
            num_served = num_served + 1
            power = compute_cost_ZR(path, modulation, network)
            cost = cost + power
            Tpb += float(i[2])/1000
    average_cost = cost / Tpb
    print(average_cost, Tpb)
    return average_cost, Tpb


def OEO_serve(network, requests):
    request_table = {}
    G = network.topology
    num_served = 0
    cost = 0
    Tpb = 0
    for i in requests:
        path, modulation = find_shortest_path_OEO(i, network)
        # sorted_modulation = collections.OrderedDict(sorted(modulation.items(), key=lambda item: item[1]['reach']))
        if len(path) > 0:
            # assign modulation

            power = OEO_serve_request(path, modulation, network)
            num_served += 1
            cost = cost + power
            Tpb += float(i[2])/1000

    average_cost = cost / Tpb
    print(Tpb, average_cost)
    return average_cost, Tpb


def opaque_serve(network, requests):
    request_table = {}
    G = network.topology
    num_served = 0
    cost = 0
    Tpb = 0
    for i in requests:
        path, modulation = find_shortest_path_opaque(i, network)
        # sorted_modulation = collections.OrderedDict(sorted(modulation.items(), key=lambda item: item[1]['reach']))
        if len(path) > 0:
            for j in range(0, len(path) - 1):
                G[path[j]][path[j + 1]]['channels'] = G[path[j]][path[j + 1]]['channels'] - math.ceil(
                    modulation[list(modulation.keys())[0]]['channel'] / 25)
                G[path[j]][path[j + 1]]['occupied_channel'] = G[path[j]][path[j + 1]]['occupied_channel'] + math.ceil(
                    modulation[list(modulation.keys())[0]]['channel'] / 25)
                G[path[j]][path[j + 1]]['occupied_requests'].append(i)
            request_table[i] = path
            num_served = num_served + 1
            power = compute_cost_opaque(path, modulation, network)
            cost = cost + power
            Tpb = Tpb + float(i[2])/1000
    average_cost = cost / Tpb
    print(average_cost, Tpb)
    return average_cost, Tpb


if __name__ == '__main__':
    zr = {}
    oeo = {}
    opaque = {}
    for i in range(0, 10):
        for init_num_request in [350,400,450,500,550,600,650,700]:
            ZR = N()
            ZR_opaque = N()
            OEO = N()
            ZR.get_topology()
            ZR_opaque.get_topology()
            OEO.get_topology()
            request_list = gen_request(init_num_request)
            # request_list = [(1,12,400,1)]
            print(request_list)
            average_cost_ZR, TB_ZR = ZR_serve(ZR, request_list)
            zr[init_num_request] = {'ave_cost': average_cost_ZR, 'TB': float(init_num_request/1000)*250}
            average_cost_OEO, TB_OEO = OEO_serve(OEO, request_list)
            oeo[init_num_request] = {'ave_cost': average_cost_OEO, 'TB': float(init_num_request/1000)*250}
            average_cost_opaque, TB_opaque = opaque_serve(ZR_opaque, request_list)
            opaque[init_num_request] = {'ave_cost': average_cost_opaque, 'TB': float(init_num_request/1000)*250}
        with open('no_grooming.txt', 'a') as file:
            file.write("ZR_bypass:\n")
            file.write(json.dumps(zr) + '\n')
            file.write("ZR_opaque:\n")
            file.write(json.dumps(opaque) + '\n')
            file.write("OEO_bypass:\n")
            file.write(json.dumps(oeo) + '\n')
            file.write("****************************\n")

    G = ZR.topology

    for u, v, data in G.edges(data=True):
        data['weight'] = 500-data['distance']

    pos = nx.spring_layout(G, weight='weight')

    # 绘制节点和边
    nx.draw(G, pos, with_labels=True)

    edge_labels = {(u, v): data['distance'] for u, v, data in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # 先保存图像
    plt.savefig('no_grooming.png')

    # 然后显示图表
    plt.show()