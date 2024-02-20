import heapq
import math
import networkx as nx
from CND_project.tools.no_grooming.ZR import generate_resource_graph, link_is_available
import uuid
from matplotlib import pyplot as plt

ZR_REACH_TABLE = {"16QAM": {"rate": 400, "channel": 75, "reach": 600},
                  "8QAM": {"rate": 300, "channel": 75, "reach": 1800},
                  "QPSK_1": {"rate": 200, "channel": 75, "reach": 3000},
                  "QPSK_2": {"rate": 100, "channel": 50, "reach": 3000}}


def path_mod_believable(G, path, mod):
    for i in range(len(path) - 1):
        src = path[i]
        dst = path[i + 1]
        for key, edge_attr in G[src][dst].items():
            if edge_attr["type"] == 'fiber':
                if edge_attr["channels"] >= math.ceil(ZR_REACH_TABLE[mod]['channel'] / 25):
                    return True

    return False


def build_virtual_graph(G, mod):
    virtual_graph = nx.MultiGraph()
    for u, v, key, data in G.edges(keys=True, data=True):
        if data['type'] == 'fiber' and data['channels'] >= math.ceil(ZR_REACH_TABLE[mod]['channel'] / 25) and data[
            'distance'] <= ZR_REACH_TABLE[mod]['reach']:
            virtual_graph.add_edge(u, v, key=key, **data)
    return virtual_graph


def light_path_available(light_path, G, mod):
    for i in range(0, len(light_path) - 1):
        u = light_path[i]
        v = light_path[i + 1]
        for u, v, key, data in G.edges(keys=True, data=True):
            if data['type'] == 'fiber' and data['channels'] >= math.ceil(ZR_REACH_TABLE[mod]['channel'] / 25):
                return True

    return False


def gene_auxiliary_graph_ZR_bypass(G, request):
    auxiliary_graph = nx.MultiGraph()
    for u, v, key, data in G.edges(keys=True, data=True):
        if data['type'] == 'fiber':
            auxiliary_graph.add_edge(u, v, key=key, **data)
    pre_reach = 0
    for key, value in enumerate(ZR_REACH_TABLE):
        mod = value
        if ZR_REACH_TABLE[value]['rate'] >= request[2]:
            virtual_edge = []
            virtual_graph = build_virtual_graph(auxiliary_graph, mod)
            reach = ZR_REACH_TABLE[value]['reach']
            for src in virtual_graph.nodes():
                for dst in virtual_graph.nodes():
                    if src != dst and nx.has_path(virtual_graph, src, dst):
                        path = nx.dijkstra_path(virtual_graph, src, dst, weight='distance')
                        distance = nx.dijkstra_path_length(virtual_graph, src, dst, weight='distance')
                        if pre_reach < distance <= reach:
                            virtual_edge.append([src, dst, distance, path, mod])
            pre_reach = reach
            for edge in virtual_edge:
                src, dst = edge[0], edge[1]
                auxiliary_graph.add_edge(src, dst, key=uuid.uuid4().hex, distance=edge[2], dependency=edge[3], mod=edge[4],
                                         type='virtual')

    for key, value in enumerate(ZR_REACH_TABLE):
        if ZR_REACH_TABLE[value]['rate'] == request[2]:
            mod = value
    for u, v, key, data in G.edges(keys=True, data=True):
        if data['type'] == 'mod_channel' and data['free_capacity'] >= request[2] and data['distance'] <= \
                ZR_REACH_TABLE[mod]['reach']:
            auxiliary_graph.add_edge(u, v, key=key, **data)

    for u, v, key, data in G.edges(keys=True, data=True):
        if data['type'] == 'fiber':
            auxiliary_graph.remove_edge(u, v, key=key)

    for node in G.nodes():
        if node not in auxiliary_graph.nodes():
            auxiliary_graph.add_node(node)

    return auxiliary_graph


def update_weight_ZR_bypass(G):
    for u, v, key, data in G.edges(keys=True, data=True):
        if data['type'] == 'mod_channel':
            G.edges[u, v, key]['weight'] = 0.001 * data['distance']
        else:
            G.edges[u, v, key]['weight'] = 0.001 * data['distance'] + 12

    return G


def grooming_available(G, u, v, rate):
    for key, edge_attr in G[u][v].items():
        if edge_attr.get('type') == 'mod_channel' and edge_attr.get('free_capacity') >= rate:
            return True
    return False


def select_grooming(G, u, v, rate):
    best_edge = None
    min_free_capacity = float('inf')

    for key, edge_attr in G[u][v].items():
        if edge_attr.get('type') == 'mod_channel' and edge_attr.get('free_capacity') >= rate:
            if edge_attr.get('free_capacity') <= min_free_capacity:
                min_free_capacity = edge_attr.get('free_capacity')
                best_edge = (u, v, key)

    return best_edge


def serve_request_ZR_bypass(G, path, request, res_path):
    build_path_list = []
    ZR = 0
    for key, value in enumerate(res_path):
        build_path_list.append(value)
    for i in range(0, len(path) - 1):
        u = path[i]
        v = path[i + 1]
        if (u, v) in build_path_list:
            light_path = res_path[(u, v)][0]
            distance = res_path[(u, v)][1]
            mod = res_path[(u, v)][2]
            G.add_edge(u, v, key=uuid.uuid4(), type='mod_channel',
                       free_capacity=ZR_REACH_TABLE[mod]['rate'] - request[2], dependency=light_path, distance=distance)
            for j in range(0, len(light_path) - 1):
                src = light_path[j]
                dst = light_path[j + 1]
                for key, edge_attr in G[src][dst].items():
                    if edge_attr.get('type') == 'fiber':
                        G[src][dst][key]['channels'] = G[src][dst][key]['channels'] - math.ceil(
                            ZR_REACH_TABLE[mod]['channel'] / 25)
            ZR = ZR + 2
        else:
            grooming_edge = select_grooming(G, u, v, request[2])
            G[grooming_edge[0]][grooming_edge[1]][grooming_edge[2]]['free_capacity'] = \
                G[grooming_edge[0]][grooming_edge[1]][grooming_edge[2]]['free_capacity'] - request[2]
    power = 6 * ZR
    return power


def reserve_path(G, path, rate):
    res_path = {}
    for i in range(0, len(path) - 1):
        u = path[i]
        v = path[i + 1]
        if not grooming_available(G, u, v, rate):
            valid_edges = []
            for key, edge_attr in G[u][v].items():
                if edge_attr.get('type') != 'mod_channel':
                    valid_edges.append([u, v, edge_attr])
            """if not valid_edges:
                continue"""
            min_distance_edge = min(valid_edges, key=lambda e: e[2]['distance'])
            res_path[(u, v)] = [min_distance_edge[2]['dependency'], min_distance_edge[2]['distance'],
                                min_distance_edge[2]['mod']]

    return res_path
