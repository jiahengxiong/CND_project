import math
import uuid

import networkx as nx

OEO_REACH_TABLE = {"PCS64QAM_1": {"rate": 800, "channel": 100, "reach": 150},
                   "PCS64QAM_2": {"rate": 700, "channel": 100, "reach": 400},
                   "16QAM_1": {"rate": 600, "channel": 100, "reach": 700},
                   "PCS16QAM_1": {"rate": 500, "channel": 100, "reach": 1300},
                   "PCS16QAM_2": {"rate": 400, "channel": 100, "reach": 2500},
                   "PCS16QAM_3": {"rate": 300, "channel": 100, "reach": 4700},
                   "64QAM": {"rate": 300, "channel": 50, "reach": 100},
                   "16QAM_2": {"rate": 200, "channel": 50, "reach": 900},
                   "QPSK": {"rate": 100, "channel": 50, "reach": 3000}}


def path_mod_believable(G, path, mod):
    for i in range(len(path) - 1):
        src = path[i]
        dst = path[i + 1]
        for key, edge_attr in G[src][dst].items():
            if edge_attr["type"] == 'fiber':
                if edge_attr["channels"] >= math.ceil(OEO_REACH_TABLE[mod]['channel'] / 25):
                    return True

    return False


def build_virtual_graph(G, mod):
    virtual_graph = nx.MultiGraph()
    for u, v, key, data in G.edges(keys=True, data=True):
        if data['type'] == 'fiber' and data['channels'] >= math.ceil(OEO_REACH_TABLE[mod]['channel'] / 25) and data[
            'distance'] <= OEO_REACH_TABLE[mod]['reach']:
            virtual_graph.add_edge(u, v, key=key, **data)
    return virtual_graph


def light_path_available(light_path, G, mod):
    for i in range(0, len(light_path) - 1):
        u = light_path[i]
        v = light_path[i + 1]
        for u, v, key, data in G.edges(keys=True, data=True):
            if data['type'] == 'fiber' and data['channels'] >= math.ceil(OEO_REACH_TABLE[mod]['channel'] / 25):
                return True

    return False


def gene_auxiliary_graph_OEO_bypass(G, request):
    auxiliary_graph = nx.MultiGraph()
    for u, v, key, data in G.edges(keys=True, data=True):
        if data['type'] == 'fiber':
            auxiliary_graph.add_edge(u, v, key=key, **data)
    for key, value in enumerate(OEO_REACH_TABLE):
        mod = value
        if OEO_REACH_TABLE[value]['rate'] >= request[2]:
            virtual_edge = []
            virtual_graph = build_virtual_graph(auxiliary_graph, mod)
            reach = OEO_REACH_TABLE[value]['reach']
            for src in virtual_graph.nodes():
                for dst in virtual_graph.nodes():
                    if src != dst and nx.has_path(virtual_graph, src, dst):
                        path = nx.dijkstra_path(virtual_graph, src, dst, weight='distance')
                        distance = nx.dijkstra_path_length(virtual_graph, src, dst, weight='distance')
                        if distance <= reach:
                            virtual_edge.append([src, dst, distance, path, mod])
            for edge in virtual_edge:
                src, dst = edge[0], edge[1]
                auxiliary_graph.add_edge(src, dst, key=uuid.uuid4().hex, distance=edge[2], dependency=edge[3],
                                         mod=edge[4],
                                         type='virtual')
    mod_list = []
    for key, value in enumerate(OEO_REACH_TABLE):
        if OEO_REACH_TABLE[value]['rate'] == request[2]:
            mod_list.append(value)
    min_reach = 100000
    for mod in mod_list:
        if OEO_REACH_TABLE[mod]['reach'] < min_reach:
            min_reach = OEO_REACH_TABLE[mod]['reach']
    for u, v, key, data in G.edges(keys=True, data=True):
        if data['type'] == 'mod_channel' and data['free_capacity'] >= request[2] and data['distance'] <= \
                min_reach:
            auxiliary_graph.add_edge(u, v, key=key, **data)

    for u, v, key, data in G.edges(keys=True, data=True):
        if data['type'] == 'fiber':
            auxiliary_graph.remove_edge(u, v, key=key)

    for node in G.nodes():
        if node not in auxiliary_graph.nodes():
            auxiliary_graph.add_node(node)

    return auxiliary_graph


def update_weight_OEO_bypass(G):
    for u, v, key, data in G.edges(keys=True, data=True):
        if data['type'] == 'mod_channel':
            G.edges[u, v, key]['weight'] = 0.0001 * data['distance']
        else:
            G.edges[u, v, key]['weight'] = 0.0001 * data['distance'] + 24 + 0.00001 * math.ceil(OEO_REACH_TABLE[data['mod']]['rate'] / 25)

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


def serve_request_OEO_bypass(G, path, request, res_path):
    build_path_list = []
    mux = 0
    traffic = 0
    for key, value in enumerate(res_path):
        build_path_list.append(value)
    for i in range(0, len(path) - 1):
        u = path[i]
        v = path[i + 1]
        if (u, v) in build_path_list:
            light_path = res_path[(u, v)][0]
            distance = res_path[(u, v)][1]
            mod = res_path[(u, v)][2]
            for j in range(0, len(light_path) - 1):
                src = light_path[j]
                dst = light_path[j + 1]
                for key, edge_attr in G[src][dst].items():
                    if edge_attr.get('type') == 'fiber':
                        G[src][dst][key]['channels'] = G[src][dst][key]['channels'] - math.ceil(
                            OEO_REACH_TABLE[mod]['channel'] / 25)
            mux = mux + 1
            traffic = traffic + 2 * OEO_REACH_TABLE[mod]['rate']
        else:
            grooming_edge = select_grooming(G, u, v, request[2])
            G[grooming_edge[0]][grooming_edge[1]][grooming_edge[2]]['free_capacity'] = \
                G[grooming_edge[0]][grooming_edge[1]][grooming_edge[2]]['free_capacity'] - request[2]
            # traffic = traffic + 2*request[2]
    power = 2 * 12 * mux + traffic * 0.01
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
            max_rate_edge = min(valid_edges, key=lambda e: e[2]['weight'])
            res_path[(u, v)] = [max_rate_edge[2]['dependency'], max_rate_edge[2]['distance'],
                                max_rate_edge[2]['mod']]

    return res_path
