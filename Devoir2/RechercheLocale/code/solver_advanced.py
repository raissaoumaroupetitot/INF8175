import random
import math
from schedule import Schedule



#----------- fonctions utiles et initialisation ------------

def greedy_color(schedule: Schedule, order: list):
    """
    Coloration de graphe gloutonne avec un ordre donné
    Pour chaque cours on assigne le plus petit créneau (dans l'ordre) qui ne crée pas de conflit avec ses voisins
    """
    graph = schedule.conflict_graph
    solution = {}
    for node in order:
        neighbor_slots = {solution[n] for n in graph.neighbors(node) if n in solution} #les crénaux des cours voisins
        slot = 1
        while slot in neighbor_slots:
            slot += 1
        solution[node] = slot
    return solution


def count_colors(solution: dict):
    """ Retourne le nombre de créneaux utilisés """
    return len(set(solution.values()))


def compress_colors(solution: dict):
    """Renumérote les créneaux de 1 à K pour supprimer les trous"""
    mapping = {c: i + 1 for i, c in enumerate(sorted(set(solution.values())))}
    return {node: mapping[c] for node, c in solution.items()}



# --------- Algorithme hill climbing ---------

def hill_climbing(schedule: Schedule, solution: dict):
    """
    Recherche locale par hill climbing
    À chaque itération on essaie de réassigner chaque cours à un créneau plus petit
    On s'arrête quand aucune amélioration n'est possible (atteinte d'un optimum local)
    """
    graph = schedule.conflict_graph
    current = dict(solution)
    improved = True #indique si on a trouvé une meilleure solution à l'itération précédente

    while improved:
        improved = False
        nodes = list(graph.nodes())
        random.shuffle(nodes)  # on veut visite tous les noeuds (voisinage connecté)

        for node in nodes:
            current_slot = current[node]
            neighbor_slots = {current[nb] for nb in graph.neighbors(node)}

            #on teste tout les créneaux plus petits
            for slot in range(1, current_slot):
                if slot not in neighbor_slots:
                    current[node] = slot
                    current = compress_colors(current)
                    improved = True
                    break
    return current



# -------- Simulated annealing -------

def simulated_annealing(schedule: Schedule, solution: dict):
    """
    Algorithme du Simulated annealing
    On accepte parfois une solution dégradante pour sortir des solutions locales
    
    """
    graph = schedule.conflict_graph
    current = dict(solution)
    best = dict(solution)
    best_k = count_colors(best)

    T = 2.0 #température initiale haute pour accepter plus
    alpha = 0.997  #facteur de refroidissement plutôt lent
    max_iter = 50000
    nodes = list(graph.nodes())

    for _ in range(max_iter):
        #on choisit un cours aléatoire
        node = random.choice(nodes)
        neighbor_slots = {current[nb] for nb in graph.neighbors(node)}
        current_k = count_colors(current)

        #Trouver les créneaux valides pas encore utilisés par les voisins
        existing_slots = set(current.values())
        valid_slots = [slot for slot in existing_slots if slot not in neighbor_slots]
        if not valid_slots: #si vide on passe
            continue

        #Proposer un nouveau créneau au hasard
        new_slot = random.choice(valid_slots)
        if new_slot == current[node]: #si c'est le même on passe
            continue

        # Appliquer le nouveau crénau
        old_slot = current[node]
        current[node] = new_slot
        current = compress_colors(current)
        new_k = count_colors(current)
        delta = new_k - current_k

        if delta < 0:
            #amélioration
            if new_k < best_k:
                best = dict(current)
                best_k = new_k
        elif delta == 0:
            #accepter avec certaine probabilité
            if random.random() >= math.exp(-1.0 / (T + 1e-10)):
                # Refuser
                current[node] = old_slot
                current = compress_colors(current)
        else:
            #Refuser
            current[node] = old_slot
            current = compress_colors(current)

        T *= alpha  # refroidissement de la température

    return best



#--------------- Solve principal -----------------

def solve(schedule: Schedule):
    """
    Your solution of the problem
    :param schedule: object describing the input
    :return: a list of tuples of the form (c,t) where c is a course and t a time slot.
    
    """
    graph = schedule.conflict_graph
    nodes = list(graph.nodes())

    #on restart un certain nombre de fois
    n_restarts = 10
    best = None
    best_k = math.inf

    for _ in range(n_restarts):
        #ordre aléatoire
        order = list(nodes)
        random.shuffle(order)

        # Initialisation
        solution = greedy_color(schedule, order)
        # Hill Climbing
        solution = hill_climbing(schedule, solution)
        
        solution = simulated_annealing(schedule, solution)

        #un dernier hill climbing après le simulated annealing
        solution = hill_climbing(schedule, solution)

        # Garder la meilleure solution trouvée
        k = count_colors(solution)
        if k < best_k:
            best = solution
            best_k = k

    return best