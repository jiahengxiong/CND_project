import math
import uuid

import networkx as nx

ZR_REACH_TABLE = {"16QAM": {"rate": 400, "channel": 75, "reach": 600},
                  "8QAM": {"rate": 300, "channel": 75, "reach": 1800},
                  "QPSK_1": {"rate": 200, "channel": 75, "reach": 3000},
                  "QPSK_2": {"rate": 100, "channel": 50, "reach": 3000}}

OEO_REACH_TABLE = {"PCS64QAM_1": {"rate": 800, "channel": 100, "reach": 150},
                   "PCS64QAM_2": {"rate": 700, "channel": 100, "reach": 400},
                   "16QAM_1": {"rate": 600, "channel": 100, "reach": 700},
                   "PCS16QAM_1": {"rate": 500, "channel": 100, "reach": 1300},
                   "PCS16QAM_2": {"rate": 400, "channel": 100, "reach": 2500},
                   "PCS16QAM_3": {"rate": 300, "channel": 100, "reach": 4700},
                   "64QAM": {"rate": 300, "channel": 50, "reach": 100},
                   "16QAM_2": {"rate": 200, "channel": 50, "reach": 900},
                   "QPSK": {"rate": 100, "channel": 50, "reach": 3000}}

OEO_ZR_REACH_TABLE = {"PCS64QAM_1": {"rate": 800, "channel": 100, "reach": 150, "device": "MUX"},
                      "PCS64QAM_2": {"rate": 700, "channel": 100, "reach": 400, "device": "MUX"},
                      "16QAM_1": {"rate": 600, "channel": 100, "reach": 700, "device": "MUX"},
                      "PCS16QAM_1": {"rate": 500, "channel": 100, "reach": 1300, "device": "MUX"},
                      "PCS16QAM_2": {"rate": 400, "channel": 100, "reach": 2500, "device": "MUX"},
                      "PCS16QAM_3": {"rate": 300, "channel": 100, "reach": 4700, "device": "MUX"},
                      "64QAM": {"rate": 300, "channel": 50, "reach": 100, "device": "MUX"},
                      "16QAM_2": {"rate": 200, "channel": 50, "reach": 900, "device": "MUX"},
                      "QPSK_3": {"rate": 100, "channel": 50, "reach": 3000, "device": "MUX"},
                      "16QAM_3": {"rate": 400, "channel": 75, "reach": 600, "device": "ZR"},
                      "8QAM": {"rate": 300, "channel": 75, "reach": 1800, "device": "ZR"},
                      "QPSK_1": {"rate": 200, "channel": 75, "reach": 3000, "device": "ZR"},
                      "QPSK_2": {"rate": 100, "channel": 50, "reach": 3000, "device": "ZR"}}


def gene_auxiliary_graph_ZR_opaque(G, request):
    # request[source, destination, rate, id]
    auxiliary_graph = nx.MultiGraph()
    for key, value in enumerate(ZR_REACH_TABLE):
        if ZR_REACH_TABLE[value]['rate'] == request[2]:
            mod = value
    for node in G.nodes():
        auxiliary_graph.add_node(node)
    for u, v, key, data in G.edges(keys=True, data=True):
        if data['type'] == 'fiber' and data['channels'] >= math.ceil(ZR_REACH_TABLE[mod]['channel'] / 25) and data[
            'distance'] <= ZR_REACH_TABLE[mod]['reach']:
            auxiliary_graph.add_edge(u, v, key=key, **data)
        elif data['type'] != 'fiber' and data['free_capacity'] >= request[2] and data['distance'] <= \
                ZR_REACH_TABLE[mod]['reach']:
            auxiliary_graph.add_edge(u, v, key=key, **data)
            continue

    return auxiliary_graph


def update_weight_ZR_opaque(G):
    for u, v, key, data in G.edges(keys=True, data=True):
        if data['type'] == 'fiber':
            G.edges[u, v, key]['weight'] = 12 + 0.0001 * data['distance']
        else:
            G.edges[u, v, key]['weight'] = 0.0001 * data['distance']

    return G


def grooming_available(G, u, v, rate):
    for key, edge_attr in G[u][v].items():
        if edge_attr.get('type') == 'mod_channel' and edge_attr.get('free_capacity') >= rate:
            # print('grooming_available:',edge_attr.get('type'), edge_attr.get('free_capacity'), rate)
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


def select_modulation_mode(G, u, v, rate):
    for key, edge_attr in G[u][v].items():
        if edge_attr.get('type') == 'fiber':
            distance = G[u][v][key]['distance']
            channels = G[u][v][key]['channels']

    best_mode = None
    max_rate = 0

    for mode, properties in ZR_REACH_TABLE.items():
        if properties['reach'] >= distance and \
                properties['rate'] >= rate and \
                math.ceil(properties['channel'] / 25) <= channels:

            if properties['rate'] >= max_rate:
                max_rate = properties['rate']
                best_mode = mode

    # print(best_mode,rate,distance,channels)

    return best_mode


def serve_request_ZR_opaque(G, path, request):
    ZR = 0
    rate = request[2]
    mod = None
    for id, key in enumerate(ZR_REACH_TABLE):
        if ZR_REACH_TABLE[key]['rate'] == rate:
            mod = key
            break
    for i in range(0, len(path) - 1):
        for key, edge_attr in G[path[i]][path[i + 1]].items():
            if edge_attr.get('type') == 'fiber':
                G[path[i]][path[i + 1]][key]['channels'] = G[path[i]][path[i + 1]][key]['channels'] - math.ceil(
                    ZR_REACH_TABLE[mod]['channel'] / 25)
        ZR += 2
    power = ZR * 6
    return power
