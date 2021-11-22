from typing import Tuple, Callable, Set, DefaultDict, FrozenSet
from collections import defaultdict
from scipy.stats import bernoulli
from functools import reduce
import random


def _get_edge(line: str) -> FrozenSet[int]:
    return frozenset([int(vertex) for vertex in line.split()])


class TriestBase:
    """
    This class implements the algorithm Triest base presented in the paper

    'L. De Stefani, A. Epasto, M. Riondato, and E. Upfal, TRIÈST: Counting Local and Global Triangles in Fully-Dynamic
    Streams with Fixed Memory Size, KDD'16.'

    The algorithm provides an estimate of the number of triangles in a graph in a streaming environment,
    where the stream represent a series of edges.
    """

    def __init__(self, file: str, M: int):
        self.file: str = file
        self.M: int = M
        self.S: Set[FrozenSet[int]] = set()
        self.t: int = 0
        self.tau_vertices: DefaultDict[int, int] = defaultdict(int)
        self.tau: int = 0

    def _sample_edge(self, edge: FrozenSet[int], t: int):
        if t < self.M:
            return True
        elif bernoulli.rvs(p=self.M / t):
            edge_to_remove: FrozenSet[int] = random.choice(list(self.S))
            self.S.remove(edge_to_remove)
            self._update_counters(lambda x, y: x - y, edge_to_remove)
        else:
            return False

    def _update_counters(self, operator: Callable[[int, int], int], edge: FrozenSet[int]):
        common_neighbourhood: Set[int] = reduce(
            lambda a, b: a & b,
            [
                {
                    node
                    for link in self.S
                    if vertex in link
                    for node in link
                    if node != vertex
                }
                for vertex in edge
            ]
        )

        for vertex in common_neighbourhood:
            self.tau = operator(self.tau, 1)
            self.tau_vertices[vertex] = operator(self.tau_vertices[vertex], 1)

            for node in edge:
                self.tau_vertices[node] = operator(self.tau_vertices[node], 1)

    def run(self):
        with open(self.file, 'r') as f:
            for line in f:
                edge = _get_edge(line)
                self.t += 1

                if self._sample_edge(edge, self.t):
                    self.S.add(edge)
                    self._update_counters(lambda x, y: x + y, edge)
