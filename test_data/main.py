import buildGraph
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.sparse import csr_matrix
import ODEModel

# Main script that runs test dynamics for example graphs.

def main():

    ### TODO: Make laplacian for weight/directed version conservative
    ### TODO: Remove sources and use deposits/withdrawals instead

    # Choose number of users and example network
    users = 10
    directed = True
    weighting = 0.5

    # Choose some time parameter
    t_start = 0
    t_end = 10
    number_of_steps = 1000000
    t_span = np.linspace(t_start, t_end, number_of_steps)

    if directed:
        user_network = buildGraph.directed_growing_network(population=users, seed=1, weighting=weighting)
        degrees = nx.degree(user_network)
        degree_diag = [degrees[degree_idx] for degree_idx in range(np.shape(degrees)[0])]
        degree_matrix = np.diag(degree_diag)
        adjacency_matrix = nx.adjacency_matrix(user_network)
        #laplacian = csr_matrix(degree_matrix) - adjacency_matrix
        laplacian = csr_matrix(nx.directed_laplacian_matrix(user_network))
    else:
        user_network = buildGraph.watts_hub(population=users, nearest_neighbors=3, prob_rewiring=0.5, seed=1, weighting=weighting)
        laplacian = nx.laplacian_matrix(user_network)



    # Place all assets in Primitive node (which is the last node)
    assets_0 = np.zeros(users)

    # Add sources of assets
    assets_sources = np.zeros(users)
    assets_sources[0] = 0.25

    # Add sinks of assets
    #N/A

    # Integrate the equation
    model = lambda y, t : ODEModel.model(y,t,L = laplacian, sources = assets_sources)
    assets = odeint(model, assets_0, t_span)
    asset_flow_plot = plt.figure(1)
    for user in range(0,users):
        plt.plot(t_span, assets[:,user])

    # Visualize graph quickly
    graph_plot = plt.figure(2)
    pos = nx.spring_layout(user_network, scale=10*users, k=10/np.sqrt(user_network.order()))
    nodes , degree = map(list, zip(*list(nx.degree(user_network))))
    nx.draw_networkx_nodes(user_network, pos, node_size=[value * 100 for value in degree])
    nx.draw_networkx_edges(user_network, pos, width=3)
    nx.draw_networkx_labels(user_network, pos, font_size=20, font_family="sans-serif")
    edge_labels = nx.get_edge_attributes(user_network, "weight")
    nx.draw_networkx_edge_labels(user_network, pos, edge_labels)
    plt.show()

if __name__ == "__main__":
    main()
