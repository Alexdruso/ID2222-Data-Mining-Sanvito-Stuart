import networkx as nx
import numpy as np
from scipy import linalg
from sklearn.cluster import KMeans
from typing import Callable, Dict

from utils import load_graph

selection_methods: Dict[str, Callable[[np.ndarray, int], int]] = {
    # +2 because 1 accounts for indices starting from 0 and 1 accounts for the fact that k is the index of the NEXT
    # eigenvalue
    'auto': lambda eigenvalues, k: np.argmin(np.ediff1d(eigenvalues)) + 2,
    'manual': lambda eigenvalues, k: k
}


def spectral_clustering(
        file: str,
        number_of_clusters_selection: str = 'auto',
        k: int = 10,
        verbose: bool = True
) -> np.ndarray:
    """
    This function implements the algorithm described in

    “On Spectral Clustering: Analysis and an algorithm” (Links to an external site.)
    by Andrew Y. Ng, Michael I. Jordan, Yair Weiss

    This function computes k clusters in the graph contained in file with spectral clustering and returns a numpy array of shape
    (number of vertices,) containing the label for each vertex.

    :param file: the path to the file representing the graph
    :param number_of_clusters_selection: either auto or manual, determines how k is selected
    :param k: the number of clusters to be identified, works if selection method is manual
    :param verbose: if true, prints updates on the status of the computation
    :return: returns a numpy array of shape
    (number of vertices,) containing the label for each vertex
    """
    if verbose:
        print('Loading graph...')

    G: nx.Graph = load_graph(file)

    if verbose:
        print('Computing clusters...')

    A = nx.to_numpy_matrix(G)
    D = np.diagflat(np.sum(A, axis=1))
    D_inv = np.linalg.inv(np.sqrt(D))
    L = D_inv @ A @ D_inv
    # returns eigenvalues and vectors in ascending order
    values, vectors = linalg.eigh(L)

    k = selection_methods[number_of_clusters_selection](values[::-1], k)

    if verbose and number_of_clusters_selection == 'auto':
        print('The estimated optimal number of clusters is {}.'.format(k))

    X = vectors[:, -k:]
    Y = X / np.linalg.norm(X, axis=1, keepdims=True)
    result = KMeans(n_clusters=k).fit(Y).labels_

    if verbose:
        print('Clusters computed.')

    return result


if __name__ == '__main__':
    result = spectral_clustering('../data/example1.dat')

    print(result.shape)
