from matplotlib import pyplot as plt

from CND_project.tools.no_grooming.network import *
from CND_project.tools.no_grooming.ZR import gen_request


def ZR_opaque_serve(network, requests):
    pass


if __name__ == '__main__':
    ZR_opaque = network()
    G = ZR_opaque.topology

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True)

    edge_labels = {(u, v): d['distance'] for u, v, d in G.edges(data=True)}

    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.show()
    ini_num_request = 250
    requests = gen_request(ini_num_request)
    ZR_opaque_serve(ZR_opaque, requests)
