from random_permutation_search import count_cost
from utils import *


def initialize_population(population_size, clients):
    population = []
    for i in range(population_size):
        random.shuffle(clients)
        population.append(list(clients))
    return population


def bests(g: nx.Graph, source, population, number_of_bests):
    sorted_elements = sorted(
        population,
        key=lambda el: count_cost(g, el, source)[1])
    return sorted_elements[0:number_of_bests]


def reproduce(population, number_of_reproduced):
    return [population[random.randint(0, len(population) - 1)] for i in range(number_of_reproduced)]


def cross(clients_list1, clients_list2):
    length = range(len(clients_list1))
    clients1_with_indices = zip(clients_list1, length)
    clients2_with_indices = zip(clients_list2, length)
    diffs = list(filter(lambda a: a[0][0] != a[1][0], zip(clients1_with_indices, clients2_with_indices)))
    diff_clients2 = list(map(lambda a: a[1], diffs))
    sorted_diffs = sorted(diffs, key=lambda tup: tup[0][0])
    indices_not_changed = list(set(length)-set(map(lambda x: x[0][1], diffs)))
    semi_result_not_changed = {}
    for i in indices_not_changed:
        semi_result_not_changed[i] = clients_list1[i]

    semi_result = {}
    for i in range(len(sorted_diffs)):
        value_to_put = diff_clients2[i][0]
        idx_to_put = sorted_diffs[i][0][1]
        semi_result[idx_to_put] = value_to_put
    semi_result.update(semi_result_not_changed)
    return list(semi_result.values())


def crossover(reproduced, crossovers_number):
    result = []
    for i in range(crossovers_number):
        clients_list1 = reproduced.pop(random.randint(0, len(reproduced)-1))
        clients_list2 = reproduced.pop(random.randint(0, len(reproduced)-1))
        crossed_element = cross(clients_list1, clients_list2)
        result.append(crossed_element)
    result += reproduced
    return result


def mutate(crossovered, probability_of_mutation):
    def mutate_element(el):
        idx1 = random.randint(0, len(el)-1)
        idx2 = random.randint(0, len(el)-1)
        el[idx1], el[idx2] = el[idx2], el[idx1]
        return el

    def should_mutate() -> bool:
        return random.random() < probability_of_mutation
    return [mutate_element(el) if should_mutate() else el for el in crossovered]


def succession(mutated, bests_elements):
    return mutated+bests_elements


def genetic_search(
        g: nx.Graph,
        source,
        iterations_number,
        population_size=10,
        crossovers_number: int=6,
        best_count=1,
        probability_of_mutation=0.05):
    """
    Algorithm:
        1. draw initial a population                                        (size X)
        2. reproduce new population                                         (size X+k-b)
        3. make 'k' crossovers of random elements                           (size X-b)
        4. mutate elements with probability of 'm'                          (size X-b)
        5. succession new population (take b best from input population)    (size X)
        6. go to step 2
    """
    clients = list(filter(lambda n: g.nodes[n]['isClient'], g.nodes))
    population = initialize_population(population_size, clients)
    for i in range(iterations_number):
        bests_elements = bests(g, source, population, best_count)
        reproduced = reproduce(population, population_size+crossovers_number-best_count)
        crossovered = crossover(reproduced, crossovers_number)
        mutated = mutate(crossovered, probability_of_mutation)
        population = succession(mutated, bests_elements)

    return count_cost(g, bests(g, source, population, 1)[0], source)
