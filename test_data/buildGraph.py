'''
Function to construct a test network for Primitive users
'''

import networkx as nx
import numpy as np


def watts_hub(population, nearest_neighbors, prob_rewiring, seed, weighting):
    ### TODO: this needs adjusted for weights still
    # Choose a simple test case of Watts-Strogatz and then add a hub representing Primitive
    G = nx.watts_strogatz_graph(n=population-1, k=nearest_neighbors, p=prob_rewiring, seed=seed)
    G.add_node(population)
    for node_idx in range(0,population-1):
        G.add_weighted_edges_from(node_idx,population,weighting)

    return G

def directed_growing_network(population, seed, weighting):

    G = nx.gn_graph(n=population-1, seed=seed)
    G.add_node(population-1)
    np.random.seed(1)
    weights = np.random.rand(population-1)
    edge_idx = 1
    for edge in G.edges():
        G[edge[0]][edge[1]]['weight'] = weights[edge_idx]
        edge_idx += 1
    for node_idx in range(0,population-1):
        G.add_edge(node_idx,population-1,weight = weighting)
        G.add_edge(population-1,node_idx,weight = weighting)

    #print(G.edges())
    #print(nx.get_edge_attributes(G,'weight'))
    return G
