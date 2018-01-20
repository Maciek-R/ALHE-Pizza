from utils import *


def shortest_paths_to_clients(g: nx.Graph, source, clients):
    paths = []
    for client in clients:
        paths.append(shortest_path_to_client(g, source, client))
    return paths


def find_real_cost(g: nx.Graph, shortest_paths, time, current_clients):
    for path in shortest_paths:
        a, b, c = get_user_parameters()
        elapsed_time = path['path_cost']
        first = a*elapsed_time
        sum_of_real_dist = 0
        for node1, node2 in take_pairs(path['path']):
            edge = find_edge(g, g.nodes[node1], g.nodes[node2])
            sum_of_real_dist += edge['distReal']
        second = b*sum_of_real_dist
        third = c*get_dissatisfaction(g, time, elapsed_time, current_clients)
        real_cost = first + second + third

        path["cost"] = real_cost
        path['elapsed_time'] = elapsed_time
    return shortest_paths


def greedy_a_star(g: nx.Graph, start_node):
    """
        Algorithm:
            1. find the shortest paths from the current node to all clients
            2. take the shortest path from step 1 and go to this client
            3. if all clients are served finish else go to the step 1
    """
    time = 0
    client_nodes = list(filter(lambda n: g.nodes[n]['isClient'], g.nodes))
    current_node = start_node
    result_path = [start_node]
    result_cost = 0
    while client_nodes:
        shortest_paths = shortest_paths_to_clients(g, current_node, client_nodes)
        shortest_paths = find_real_cost(g, shortest_paths, time, client_nodes)
        shortest_path = min(shortest_paths, key=lambda x: x['cost'])
        time += shortest_path['elapsed_time']
        current_client = shortest_path['client']
        client_nodes.remove(current_client)
        result_path += shortest_path['path'][1:]
        current_node = current_client
        result_cost += shortest_path['cost']
    return result_path, result_cost


