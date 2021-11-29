import networkx as nx


def load_graph(file: str) -> nx.Graph:
    """
    This function takes as input the path to a file containing a list of edges in a graph and outputs the
    graph in the form of a networkx class.

    :param file: the path to the file representing the graph
    :return: a nx.Graph instance representing the graph
    """
    return nx.read_edgelist(
        path=file,
        delimiter=','
    )


if __name__ == '__main__':
    G = load_graph('../data/example1.dat')

    print('The size of the graph is {}.'.format(G.size()))
