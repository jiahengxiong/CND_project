import networkx as nx
import matplotlib.pyplot as plt
from tools.no_grooming.network import Continental_network, National_network


German = National_network().topology
Eu = Continental_network().topology


def get_edge_distance(graph, u, v):
    edge_data = graph.get_edge_data(u, v)
    if edge_data:
        return edge_data[list(edge_data.keys())[0]].get('distance', 1)  # Default to 1 if distance is not available
    else:
        return 1



plt.figure(figsize=(10, 6))
edge_lengths_german = {(u, v): 450 - get_edge_distance(German, u, v) for u, v in German.edges()}
max_distance_german = max(edge_lengths_german.values())
pos_german = nx.spring_layout(German, weight='distance', iterations=10000, scale=1)


pos_german = {node: (x * max_distance_german, y * max_distance_german) for node, (x, y) in pos_german.items()}

nx.draw(German, pos_german, with_labels=True, node_size=200, node_color='skyblue', font_size=12)

edge_labels_german = {(u, v): get_edge_distance(German, u, v) for u, v in German.edges()}
nx.draw_networkx_edge_labels(German, pos_german, edge_labels=edge_labels_german, font_color='red')

plt.title('German Network')
plt.savefig('german_network.png')
plt.show()


plt.figure(figsize=(12, 8))
edge_lengths_eu = {(u, v): get_edge_distance(Eu, u, v) for u, v in Eu.edges()}
max_distance_eu = max(edge_lengths_eu.values())
pos_eu = nx.spring_layout(Eu, weight='distance', iterations=10000, scale=1)


pos_eu = {node: (x * max_distance_eu, y * max_distance_eu) for node, (x, y) in pos_eu.items()}

nx.draw(Eu, pos_eu, with_labels=True, node_size=50, node_color='skyblue', font_size=12)

edge_labels_eu = {(u, v): get_edge_distance(Eu, u, v) for u, v in Eu.edges()}
nx.draw_networkx_edge_labels(Eu, pos_eu, edge_labels=edge_labels_eu, font_color='red')

plt.title('European Network')
plt.savefig('european_network.png')
plt.show()
