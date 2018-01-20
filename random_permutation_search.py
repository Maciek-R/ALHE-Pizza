from utils import *


def change_random_elements(client_nodes):
    list_len = len(client_nodes) - 1
    idx1 = random.randint(0, list_len)
    idx2 = random.randint(0, list_len)
    client_nodes[idx1], client_nodes[idx2] = client_nodes[idx2], client_nodes[idx1]
    return client_nodes


def random_permutation_search(g: nx.Graph, start_node, steps=1000):
    """
        Algorithm:
            1. initialize population
            1. randomize permutation of clients
            2. for current permutation find the cost, if it's better than the best => save result else nothing
            3. go to step 2
    """
    client_nodes = list(filter(lambda n: g.nodes[n]['isClient'], g.nodes))
    random.shuffle(client_nodes)
    best_path, best_cost = count_cost(g, client_nodes, start_node)
    for i in range(steps):
        client_nodes = change_random_elements(list(client_nodes))
        path, cost = count_cost(g, client_nodes, start_node)
        if cost < best_cost:
            best_path, best_cost = path, cost
    return best_path, best_cost
