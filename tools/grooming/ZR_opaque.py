import heapq
import math
import networkx as nx
import uuid
from matplotlib import pyplot as plt

ZR_REACH_TABLE = {"16QAM": {"rate": 400, "channel": 75, "reach": 600},
                  "8QAM": {"rate": 300, "channel": 75, "reach": 1800},
                  "QPSK_1": {"rate": 200, "channel": 75, "reach": 3000},
                  "QPSK_2": {"rate": 100, "channel": 50, "reach": 3000}}


def gene_auxiliary_graph(G, request):
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
        elif data['type'] != 'fiber' and data['free_capacity'] >= request[2] and data['distance'] <= ZR_REACH_TABLE[mod]['reach']:
            auxiliary_graph.add_edge(u, v, key=key, **data)
            continue

    return auxiliary_graph


def update_weight(G):
    for u, v, key, data in G.edges(keys=True, data=True):
        if data['type'] == 'fiber':
            G.edges[u, v, key]['weight'] = 12 + 0.0001 * data['distance']
        else:
            G.edges[u, v, key]['weight'] = 0.0001 * data['distance']

    return G


def grooming_available(G, u, v, rate):
    for key, edge_attr in G[u][v].items():
        if edge_attr.get('type') == 'mod_channel' and edge_attr.get('free_capacity') >= rate:
            #print('grooming_available:',edge_attr.get('type'), edge_attr.get('free_capacity'), rate)
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

    #print(best_mode,rate,distance,channels)

    return best_mode


# Make sure to pass the graph G, nodes u and v, and the required rate when calling the function
# Example call: select_modulation_mode(G, 'u', 'v', 150)

def serve_request(G, path, request):
    ZR = 0
    for i in range(0, len(path) - 1):
        if grooming_available(G, path[i], path[i + 1], request[2]):
            grooming_edge = select_grooming(G, path[i], path[i + 1], request[2])
            G[grooming_edge[0]][grooming_edge[1]][grooming_edge[2]]['free_capacity'] -= request[2]
            G[grooming_edge[0]][grooming_edge[1]][grooming_edge[2]]['request'].append(request)
        else:
            edge = 0
            for key, edge_attr in G[path[i]][path[i + 1]].items():
                if edge_attr.get('type') == 'fiber':
                    edge = key
            mod = select_modulation_mode(G, path[i], path[i + 1], request[2])
            G.add_edge(path[i], path[i + 1], type='mod_channel',
                       channels=math.ceil(ZR_REACH_TABLE[mod]['channel'] / 25),
                       free_capacity=ZR_REACH_TABLE[mod]['rate'] - request[2],
                       key=uuid.uuid4().hex,
                       distance=G[path[i]][path[i + 1]][edge]['distance'],
                       request=[request])
            for key, edge_attr in G[path[i]][path[i + 1]].items():
                if edge_attr.get('type') == 'fiber':
                    G[path[i]][path[i + 1]][key]['channels'] = G[path[i]][path[i + 1]][key]['channels'] - math.ceil(
                        ZR_REACH_TABLE[mod]['channel'] / 25)
            ZR += 2
    power = ZR*6
    return power
