import networkx as nx


def load_graph(file: str) -> nx.Graph:
    return nx.read_edgelist(
        path=file,
        delimiter=','
    )


if __name__ == '__main__':
    G = load_graph('../data/example1.dat')

    print('The size of the graph is {}.'.format(G.size()))
