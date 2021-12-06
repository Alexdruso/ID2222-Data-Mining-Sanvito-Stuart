import networkx as nx


def load_graph(file: str, weight: bool = False) -> nx.Graph:
    """
    This function takes as input the path to a file containing a list of edges (and optionally weights)
    in a graph and outputs the graph in the form of a networkx class.

    :param file: the path to the file representing the graph
    :param weight: indicates if the file contains edge weights or not
    :return: a nx.Graph instance representing the graph
    """

    if weight:
        return nx.read_weighted_edgelist(
            path=file,
            delimiter=','
        )
    else:
        return nx.read_edgelist(
            path=file,
            delimiter=','
        )


if __name__ == '__main__':
    G = load_graph('../data/example1.dat')

    print('The size of the graph is {}.'.format(G.size()))
