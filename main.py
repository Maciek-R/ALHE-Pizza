from multiprocessing import Process
import csv
import matplotlib.pyplot as plt
from networkx import Graph

from greedy_a_star import greedy_a_star
from random_permutation_search import random_permutation_search
from utils import *
from genetic_search import genetic_search

def print_nodes(graph: Graph):
    [print(node, g.nodes[node]) for node in graph.nodes]


def print_edges(graph: Graph):
    [print(edge, g.edges[edge]) for edge in graph.edges]


def create_n_node_complete_graph(nodes_with_attributes):
    """ Parameters
        ----------
        nodes_with_attributes: input list
            Data that contains triple of index, x and y."""
    g = nx.Graph(None, clientNo=0)
    client_no = 0
    for node, x, y, is_client in nodes_with_attributes:
        if is_client:
            client_no += 1
        g.add_node(node, id=node, x=x, y=y, isClient=is_client, fun=take_randomly(), parent="None")

    g.graph['clientNo'] = client_no
    add_edges(g, create_edges(len(nodes_with_attributes)))
    nx.write_gml(g, 'asd')
    return g


def create_edges(n):
    return [(a+1, b+1) for a in range(n) for b in range(a+1, n)]


def find_neiber(node, g: Graph, sorted_edges, explored):
    node_id = node['id']

    def count_goal(node_dest):
        c_value, time = c_foo(node, node_dest, g)
        goal_val = h_foo(g, sorted_edges) + c_value
        node_dest['goal_val'] = goal_val
        node_dest['c_val'] = c_value
        node_dest['parent'] = node['id']
        node_dest['time'] = node['time']+time
        return node_dest

    def good_edge(edge):
        x, y = edge
        explored_nodes = list(map(lambda node: node['id'], explored))
        return (x == node_id or y == node_id) and x not in explored_nodes and y not in explored_nodes
    good_edges = list(filter(good_edge, g.edges))
    nodes = list(map(lambda edge: g.nodes[edge[0]] if edge[1] == node_id else g.nodes[edge[1]], good_edges))
    result = list(map(count_goal, nodes))
    return result


def add_unique_to_list(enqueued, neighbors):
    for n in neighbors:
        if n not in enqueued:
            enqueued.append(n)
    return enqueued


def own_greedy_algorithm(graph: Graph, source_node, sorted_edges, path):
    """ The main rule is that the given graph is a complete graph.
        What's more we can't visit particular node twice."""
    s_node = graph.nodes[source_node]
    s_node['goal_val'] = 0
    s_node['c_val'] = 0
    s_node['time'] = 0
    enqueued = [s_node]
    explored = []
    visited_clients = 0
    while visited_clients < graph.graph['clientNo']:
        enqueued = sorted(enqueued, key=lambda node: node['goal_val'])
        new_to_expand = enqueued[0]
        if new_to_expand['isClient']:
            visited_clients += 1
        neighbors = find_neiber(new_to_expand, graph, sorted_edges, explored)
        enqueued = add_unique_to_list(enqueued, neighbors)
        explored.append(new_to_expand)
        enqueued.remove(new_to_expand)
    return list(map(lambda n: n['id'], explored))


def h_foo(g: Graph, sorted_edges):
    client_number = g.graph['clientNo']
    expanded_edges = list(map(lambda edge: g.edges[edge], sorted_edges))
    return sum(list((map(lambda edg: edg['distReal']*edg['trafficRate'], expanded_edges)))[0: client_number])


def get_dissatisfaction(g, node, time_accumulated, time):
    fun = fun_resolver(g.nodes[node]['fun'])
    return fun(time+time_accumulated) - fun(time_accumulated)


def c_foo(node_s, node_d, g):
    parent_cost = node_s['c_val']
    a, b, c = get_user_parameters()
    edge = find_edge(g, node_s, node_d)
    dist_real = edge['distReal']
    first = a*dist_real*edge['trafficRate']  # in real dist_real is the time needed to get to the node
    second = b*dist_real
    third = c*sum(
        list(map(lambda node: get_dissatisfaction(g, node, node_s['time'], dist_real*edge['trafficRate']),
                 list(filter(lambda node: g.nodes[node]['parent'] is not "None" and g.nodes[node]['isClient'], g.nodes)))))

    return first + second + third + parent_cost, dist_real*edge['trafficRate']


def resolve_path(g, source, dest):
    child_node = g.nodes[dest]
    path = [dest]
    parent = child_node['parent']
    while parent != source:
        path.append(parent)
        parent = g.nodes[parent]['parent']
    path.append(source)
    path.reverse()
    return path


def convert_from_path(g, final_path):
    result = []
    for v, w in list(zip(final_path[:-1], final_path[1:])):
        result.append((v, w))
    return result


def diff_of_edges(edges, final_edges):
    final_edges_swapped = set(map(lambda edge: (edge[1], edge[0]), final_edges))
    return edges - final_edges - final_edges_swapped


def add_edge_labels(g):
    res = dict()
    for edge in g.edges:
        edg = g.edges[edge]
        res[edge] = (edg['distReal']*edg['trafficRate'], edg['distReal'])
    return res


def own_heuristic_function(g: nx.Graph):
    path = []
    sorted_edges = list(g.edges)
    sorted_edges = sorted(sorted_edges, key=lambda edge: g.edges[edge]['distReal']*g.edges[edge]['trafficRate'])

    result = own_greedy_algorithm(g, 5, sorted_edges, path)
    final_path = resolve_path(g, result[0], result[-1])
    draw_graph(g, final_path)


def draw_graph(g: nx.Graph, final_path):
    pos = nx.spring_layout(g)
    nx.draw_networkx_nodes(
        g, pos, nodelist=list(filter(lambda node: g.nodes[node]['isClient'], g.nodes)),
        node_color='#FFAA23')
    nx.draw_networkx_nodes(
        g, pos, nodelist=list(filter(lambda node: not g.nodes[node]['isClient'], g.nodes)),
        node_color='#AE3F23')
    nx.draw_networkx_labels(g, pos)
    final_edges = convert_from_path(g, final_path)
    nx.draw_networkx_edges(g, pos, final_edges, edge_color='#FF0000')
    nx.draw_networkx_edges(g, pos, diff_of_edges(g.edges, final_edges), edge_color='#AAAAAA')
    nx.draw_networkx_edge_labels(g, pos, add_edge_labels(g), 0.2, 8)

    plt.show()


def draw_graph_with_positions(g: nx.Graph, final_path, title):
    scale = 1000
    pos = nx.spring_layout(g)
    for n in g.nodes:
        g.add_node(n=n, x=scale * np.float(pos[n][0]), y=scale * np.float(pos[n][1]))
    nx.draw_networkx_nodes(
        g, pos, nodelist=list(filter(lambda node: g.nodes[node]['isClient'], g.nodes)),
        node_color='#FFAA23')
    nx.draw_networkx_nodes(
        g, pos, nodelist=list(filter(lambda node: not g.nodes[node]['isClient'], g.nodes)),
        node_color='#AE3F23')
    nx.draw_networkx_labels(g, pos)
    final_edges = convert_from_path(g, final_path)
    nx.draw_networkx_edges(g, pos, final_edges, edge_color='#FF0000')
    nx.draw_networkx_edges(g, pos, diff_of_edges(g.edges, final_edges), edge_color='#AAAAAA')
    nx.draw_networkx_edge_labels(g, pos, add_edge_labels(g), 0.2, 3)
    nx.draw_networkx_nodes(g, pos, nodelist=[final_path[0]], node_color='#000FFF')
    plt.title(title)
    plt.show()


def create_simple_graph():
    g = create_n_node_complete_graph([
        (1, 20, 80, False),
        (2, 50, 100, False),
        (3, 60, 80, False),
        (4, 900, 500, True),
        (5, 15, 30, False),
        (6, 1500, 400, True)])
    return g


def process_greedy_a_star(g: nx.Graph):
    path, cost = greedy_a_star(g, 5)
    print('greedy', path, cost)
    draw_graph_with_positions(g, path, 'a_star')


def process_random_search(g: nx.Graph):
    path, cost = random_permutation_search(g, 5)
    print('random', path, cost)
    draw_graph_with_positions(g, path, 'random')


def process_genetic_search(g: nx.Graph):
    path, cost = genetic_search(
        g, 5, 100,
        population_size=50,
        crossovers_number=35,
        best_count=3,
        probability_of_mutation=0.1)
    print('genetic', path, cost)
    draw_graph_with_positions(g, path, 'genetic')


def load_graph(file_name):
    g = nx.read_gml(file_name, )
    return g


def load_graph(csv_file_name):
    graph = {}
    node = {}
    edge = {}
    is_graph, is_node, is_edge = False, False, False
    f = open(csv_file_name, 'rt')
    try:
        reader = csv.reader(f)
        for row in reader:
            if row == ['---g']:
                is_graph = True
            elif row == ['---n']:
                is_node = True
                is_graph = False
            elif row == ['---e']:
                is_edge = True
                is_node = False
            elif is_graph:
                graph['clientNo'] = row[0]
            elif is_node:
                id, label, x, y, parent, fun, isClient = row
                node[int(id)] = {'label': label,
                                 'x': float(x),
                                 'y': float(y),
                                 'parent': parent,
                                 'fun': int(fun),
                                 'isClient': int(isClient)}
            elif is_edge:
                source, target, distReal, trafficRate, dist = row
                edge[(int(source), int(target))] = {'dist': float(dist),
                                 'trafficRate': float(trafficRate),
                                 'distReal': float(distReal)}

    finally:
        f.close()
    number_of_nodes = len(node.keys())
    clients_number = graph['clientNo']
    g = nx.Graph(None, clientNo=clients_number)
    position = nx.spring_layout(g)
    for i in range(number_of_nodes):
        is_client = node[i]['isClient']
        g.add_node(i, id=i, x=node[i]['x'], y=node[i]['y'],
                   isClient=is_client, fun=node[i]['fun'], parent="None")
    clients_number = graph['clientNo']
    add_edges_from_file(g, edge)
    return g


if __name__ == "__main__":
    g = create_random_graph(20)
    gF = create_n_node_complete_graph([
        (1, 20, 80, False),
        (2, 50, 100, False),
        (3, 60, 80, True),
        (4, 900, 500, True),
        (5, 15, 30, False),
        (6, 1500, 400, True)])

    gl = load_graph('graf.csv')
    # p1 = Process(target=own_heuristic_function, args=(gl,))
    # p1.start()

    p2 = Process(target=process_greedy_a_star, args=(gl,))
    p2.start()

    p3 = Process(target=process_random_search, args=(gl,))
    p3.start()

    p4 = Process(target=process_genetic_search, args=(gl,))
    p4.start()

    p4.join()
    p3.join()
    p2.join()
    # p1.join()


