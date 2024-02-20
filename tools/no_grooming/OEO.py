import heapq
import math

from CND_project.tools.no_grooming.ZR import generate_resource_graph, link_is_available

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

OEO_ZR_REACH_TABLE = {"PCS64QAM_1": {"rate": 800, "channel": 100, "reach": 150},
                      "PCS64QAM_2": {"rate": 700, "channel": 100, "reach": 400},
                      "16QAM_1": {"rate": 600, "channel": 100, "reach": 700},
                      "PCS16QAM_1": {"rate": 500, "channel": 100, "reach": 1300},
                      "PCS16QAM_2": {"rate": 400, "channel": 100, "reach": 2500},
                      "PCS16QAM_3": {"rate": 300, "channel": 100, "reach": 4700},
                      "64QAM": {"rate": 300, "channel": 50, "reach": 100},
                      "16QAM_2": {"rate": 200, "channel": 50, "reach": 900},
                      "QPSK_3": {"rate": 100, "channel": 50, "reach": 3000},
                      "16QAM_3": {"rate": 400, "channel": 75, "reach": 600},
                      "8QAM": {"rate": 300, "channel": 75, "reach": 1800},
                      "QPSK_1": {"rate": 200, "channel": 75, "reach": 3000},
                      "QPSK_2": {"rate": 100, "channel": 50, "reach": 3000}}


def find_shortest_path_OEO(request, network):
    # request[source, destination, rate, id]
    requests = {"source": request[0], "destination": request[1], "rate": request[2], "id": request[3]}
    modulation = {}
    for num, mod in enumerate(OEO_REACH_TABLE):
        if OEO_REACH_TABLE[mod]['rate'] == requests['rate']:
            modulation[mod] = OEO_REACH_TABLE[mod]
    G = generate_resource_graph(network)
    start = requests["source"]
    end = requests["destination"]
    # modified dijkstra
    distances = {node: float('infinity') for node in G.nodes}
    previous_nodes = {node: None for node in G.nodes}
    distances[start] = 0
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_node == end:
            break

        if current_node not in G:
            print(f"Node {current_node} is not in the graph.")
            return [], modulation

        for neighbor in G.neighbors(current_node):
            edge_data = G.get_edge_data(current_node, neighbor)
            tentative_distance = current_distance + edge_data['distance']
            if link_is_available(modulation, edge_data):
                if tentative_distance < distances[neighbor]:
                    distances[neighbor] = tentative_distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(priority_queue, (tentative_distance, neighbor))

    path = []
    current_node = end
    if current_node in previous_nodes and previous_nodes[current_node] is not None:
        while current_node is not None:
            path.insert(0, current_node)
            current_node = previous_nodes.get(current_node, None)
        return path, modulation
    else:
        print(f"No path found from node {start} to node {end}")
        return [], modulation


def channel_min(G, u, v, path):
    channel = []
    for i in range(u, v):
        channel.append(G[path[i]][path[i + 1]]['channels'])
    min_channel = min(channel)
    return min_channel


def build_distance(path, network):
    distance_table = {}
    G = network.topology
    for i in range(0, len(path) - 1):
        distance_table[path[i]] = {}
        cumulative_distance = 0
        for j in range(i + 1, len(path)):
            cumulative_distance += G[path[j - 1]][path[j]]['distance']
            min_channel = channel_min(G, i, j, path)
            distance_table[path[i]][path[j]] = [cumulative_distance, min_channel]
    return distance_table


def update_network(u, path, mod_reach, mod_keys, modulation, network):
    G = network.topology
    print(u, mod_reach)
    if mod_reach.count(max(mod_reach)) == 1 or len(mod_reach) == 1:
        mod = mod_keys[mod_reach.index(max(mod_reach))]
        for i in range(u, max(mod_reach)):
            G[path[i]][path[i + 1]]['channels'] = G[path[i]][path[i + 1]]['channels'] - math.ceil(
                modulation[mod]['channel'] / 25)
            G[path[i]][path[i + 1]]['occupied_channel'] = G[path[i]][path[i + 1]]['occupied_channel'] + math.ceil(
                modulation[mod]['channel'] / 25)
    else:
        max_reach = max(mod_reach)
        channel = []
        for i in range(0, len(mod_reach)):
            if mod_reach[i] == max_reach:
                channel.append(modulation[mod_keys[i]]['channel'])

        min_channel = min(channel)
        for i in range(u, max(mod_reach)):
            G[path[i]][path[i + 1]]['channels'] = G[path[i]][path[i + 1]]['channels'] - math.ceil(
                min_channel / 25)
            G[path[i]][path[i + 1]]['occupied_channel'] = G[path[i]][path[i + 1]]['occupied_channel'] + math.ceil(
                min_channel / 25)


def OEO_serve_request(path, modulation, network):
    print(path, modulation)
    distance_table = build_distance(path, network)
    print(distance_table)
    mod_keys = list(modulation.keys())
    print(mod_keys)
    """modulation = {'PCS16QAM_3': {'rate': 300, 'channel': 100, 'reach': 400},
                  '64QAM': {'rate': 300, 'channel': 50, 'reach': 200}}"""

    mux = 1
    i = 0
    while i < len(path) - 1:
        mod_reach = [0 for _ in range(len(mod_keys))]
        for m in range(len(mod_keys)):
            for j in range(i + 1, len(path)):
                if distance_table[path[i]][path[j]][0] > modulation[mod_keys[m]]['reach'] or \
                        distance_table[path[i]][path[j]][1] < math.ceil(modulation[mod_keys[m]][
                                                                            'channel'] / 25):
                    mod_reach[m] = j - 1
                    break
                mod_reach[m] = j
        mux = mux + 1
        update_network(i, path, mod_reach, mod_keys, modulation, network)
        i = max(mod_reach)
    print('mux:', mux)

    power = 12 * mux + mux * modulation[mod_keys[0]]['rate']/100
    return power

