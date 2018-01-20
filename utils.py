import os
import random
from math import sqrt
from pathlib import Path

import networkx as nx
import numpy as np

import config


def count_cost(g, client_nodes, start_node):
    time = 0
    client_nodes_with_start_node = [start_node] + client_nodes
    result_path = [start_node]
    result_cost = 0
    for n1, n2 in take_pairs(client_nodes_with_start_node):
        shortest_path = shortest_path_to_client(g, n1, n2)
        shortest_path = find_real_cost_for_path(g, shortest_path, time, client_nodes)
        result_cost += shortest_path['cost']
        time += shortest_path['elapsed_time']
        result_path += shortest_path['path'][1:]
    return result_path, result_cost


def path_time_cost(g, path):
    result_cost = 0
    for n1, n2 in take_pairs(path):
        edge = find_edge(g, g.nodes[n1], g.nodes[n2])
        print('asdasdasdas', edge)
        result_cost += edge['distReal']*edge['trafficRate']
    return result_cost


def find_real_dist(g: nx.Graph, node, target):
    x, y = g.nodes[node]['x'], g.nodes[node]['y']
    x2, y2 = g.nodes[target]['x'], g.nodes[target]['y']
    return sqrt((x-x2)**2 + (y-y2)**2)


def shortest_path_to_client(g: nx.Graph, source, client):
    def heuristic(node, target):
        return find_real_dist(g, node, target)
    path = nx.astar_path(g, source, client, heuristic, weight='cost')
    path_length = path_time_cost(g, path)
    result = {"path": path, "path_cost": path_length, "client": client}
    return result


def find_edge(g, node1, node2):
    def equals(e):
        n1, n2 = e
        return (n1 == node1['id'] and n2 == node2['id']) or (n1 == node2['id'] and n2 == node1['id'])
    return g.edges[list(filter(lambda e: equals(e), g.edges))[0]]


def get_user_parameters():
    return config.a, config.b, config.c


def take_randomly():
    return random.randint(1, 2)


def fun_resolver(n):
    if n == 1:
        return square_dissat()
    else:
        return linear_dissat()


def linear_dissat():
    def foo(time):
        return time/1000.0
    return foo


def square_dissat():
    def foo(time):
        return (time/1000.0)*(time/1000.0)
    return foo


def add_edges(graph: nx.Graph, edges_pairs):
    """ Parameters
            ----------
        edges_pairs: input list
            Data that contains: node A, node B."""
    for n1, n2 in edges_pairs:
        x1 = graph.nodes[n1]['x']
        y1 = graph.nodes[n1]['y']
        x2 = graph.nodes[n2]['x']
        y2 = graph.nodes[n2]['y']
        dist = sqrt((x1-x2)**2 + (y1-y2)**2)
        dist_real = dist*random.uniform(1.1, 1.5)
        traffic_rate = random.uniform(1.0, 5.0)
        graph.add_edge(n1, n2, dist=dist, distReal=dist_real, trafficRate=traffic_rate)


def add_edges_from_file(graph: nx.Graph, edges):
    for n1, n2 in edges:
        dist = edges[(n1, n2)]['dist']
        dist_real = edges[(n1, n2)]['distReal']
        traffic_rate = edges[(n1, n2)]['trafficRate']
        graph.add_edge(n1, n2, dist=dist, distReal=dist_real, trafficRate=traffic_rate)


def save_graph_to_file(g: nx.Graph):
    file_name = 'newGraph'
    version = 0
    current_path = os.path.dirname(os.path.abspath(__file__))
    current_path_with_file_name = "{}/{}{}".format(current_path, file_name, version)
    my_file = Path(current_path_with_file_name)
    while my_file.is_file():
        version += 1
        current_path_with_file_name = "{}/{}{}".format(current_path, file_name, version)
        my_file = Path(current_path_with_file_name)

    nx.write_gml(g, current_path_with_file_name)


def take_pairs(list):
    result_list = []
    for v, w in zip(list[:-1], list[1:]):
        result_list.append([v, w])
    return result_list


def get_dissatisfaction(g, time, elapsed_time, current_clients):
    dissatisfaction = 0
    for client in current_clients:
        fun = fun_resolver(g.nodes[client]['fun'])
        dissatisfaction += fun(time+elapsed_time) - fun(time)
    return dissatisfaction


def find_real_cost_for_path(g: nx.Graph, shortest_path, time, current_clients):
    a, b, c = get_user_parameters()
    elapsed_time = shortest_path['path_cost']
    first = a * elapsed_time
    sum_of_real_dist = 0
    for node1, node2 in take_pairs(shortest_path['path']):
        edge = find_edge(g, g.nodes[node1], g.nodes[node2])
        sum_of_real_dist += edge['distReal']
    second = b * sum_of_real_dist
    third = c * get_dissatisfaction(g, time, elapsed_time, current_clients)
    real_cost = first + second + third
    shortest_path["cost"] = real_cost
    shortest_path['elapsed_time'] = elapsed_time
    return shortest_path


def create_random_graph(number_of_nodes=50, min_number_of_clients=3):
    assert(number_of_nodes > min_number_of_clients)
    scale = 10000
    g = nx.connected_watts_strogatz_graph(number_of_nodes, 5, .5, tries=100, seed=None)
    position = nx.spring_layout(g)
    for i in range(number_of_nodes):
        is_client = True if not random.randint(0, 5) or number_of_nodes-i <= min_number_of_clients else False
        g.add_node(i, id=i, x=scale * np.float(position[i][0]), y=scale * np.float(position[i][1]),
                   isClient=is_client, fun=take_randomly(), parent="None")
    clients_number = len(list(filter(lambda n: g.nodes[n]['isClient'], g.nodes)))
    g.graph['clientNo'] = clients_number
    add_edges(g, g.edges)

    save_graph_to_file(g)
    # nx.draw(g, position, with_labels=True, font_weight='bold')
    # plt.show()
    return g
