import networkx as nx
from utils.network import network as N
import random



def gen_request(num):
    rate_list = [100, 200, 300, 400]
    request = []
    for i in range(0, num):
        src, dst = random.sample(range(1, 8), 2)
        rate = random.randint(0, 3)

        request.append((src, dst, rate_list[rate]))

    return request

def ZR_serve(G, requests):
    pass


if __name__ == '__main__':
    ZR = N()
    ZR_OEO = N()
    OEO = N()
    ZR.get_topology()
    ZR_OEO.get_topology()
    OEO.get_topology()

    init_num_request = 350
    request_list = gen_request(init_num_request)

    ZR_serve(ZR, request_list)


