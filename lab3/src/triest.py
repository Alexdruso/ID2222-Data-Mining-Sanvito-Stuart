from typing import Tuple, Callable, Set, DefaultDict, FrozenSet
from collections import defaultdict
from scipy.stats import bernoulli
from functools import reduce
import random


def _get_edge(line: str) -> FrozenSet[int]:
    return frozenset([int(vertex) for vertex in line.split()])


class Triest:
    """
    Blueprint for triest triangle estimation method.
    """

    def __init__(self, file: str, M: int, verbose: bool = True):
        """
        This function initializes the class with all counters set to zero. Moreover, it initializes the file path
        to file and the memory size to M.

        :param file: the path to the file to be read
        :param M: the size of the memory for the algorithm
        :param verbose: if true, prints information on screen
        """
        self.file: str = file
        self.M: int = M
        self.verbose = verbose
        self.S: Set[FrozenSet[int]] = set()
        self.t: int = 0
        self.tau_vertices: DefaultDict[int, int] = defaultdict(int)
        self.tau: int = 0

    @property
    def xi(self) -> float:
        return max(
            1.0,
            (self.t * (self.t - 1) * (self.t - 2)) /
            (self.M * (self.M - 1) * (self.M - 2))
        )

    def _sample_edge(self, t: int) -> bool:
        """
        This function determines if the new edge can be inserted in memory. If yes and if the memory if full,
        the function proceeds to remove a random edge from the memory to make space.

        :param edge: the current sample under consideration
        :param t: the number of observed samples in the stream
        :return: true if the new edge can be inserted in the memory, false otherwise
        """
        if t <= self.M:
            return True
        elif bernoulli.rvs(p=self.M / t):
            edge_to_remove: FrozenSet[int] = random.choice(list(self.S))
            self.S.remove(edge_to_remove)
            self._update_counters(lambda x, y: x - y, edge_to_remove)
            return True
        else:
            return False

    def _update_counters(self, operator: Callable[[int, int], int], edge: FrozenSet[int]) -> None:
        """
        This function updates the counters related to estimating the number of triangles. The update happens through
        the operator lambda and involves the edge and its neighbours.

        :param operator: the lambda used to update the counters
        :param edge: the edge interested in the update
        :return: nothing
        """
        common_neighbourhood: Set[int] = reduce(
            lambda a, b: a & b,
            [
                {
                    node
                    for link in self.S if vertex in link
                    for node in link if node != vertex
                }
                for vertex in edge
            ]
        )

        for vertex in common_neighbourhood:
            self.tau = operator(self.tau, 1)
            self.tau_vertices[vertex] = operator(self.tau_vertices[vertex], 1)

            for node in edge:
                self.tau_vertices[node] = operator(self.tau_vertices[node], 1)


class TriestBase(Triest):
    """
        This class implements the algorithm Triest base presented in the paper

        'L. De Stefani, A. Epasto, M. Riondato, and E. Upfal, TRIÈST: Counting Local and Global Triangles in Fully-Dynamic
        Streams with Fixed Memory Size, KDD'16.'

        The algorithm provides an estimate of the number of triangles in a graph in a streaming environment,
        where the stream represent a series of edges.
    """

    def run(self) -> float:
        """
        Runs the algorithm from the stream on the file.

        :return: the estimated number of triangles
        """

        if self.verbose:
            print("Running the algorithm with M = {}.".format(self.M))

        with open(self.file, 'r') as f:
            if self.verbose:
                print("File opened, processing the stream...")

            for line in f:
                edge = _get_edge(line)
                self.t += 1

                if self.verbose and self.t % 1000 == 0:
                    print("Currently sampling element {} in the stream.".format(self.t))

                if self._sample_edge(self.t):
                    self.S.add(edge)
                    self._update_counters(lambda x, y: x + y, edge)

                if self.verbose and self.t % 1000 == 0:
                    print("The current estimate for the number of triangles is {}.".format(
                        self.xi * self.tau)
                    )

            return self.xi * self.tau


class TriestImproved(Triest):
    """
        This class implements the algorithm Triest improved presented in the paper

        'L. De Stefani, A. Epasto, M. Riondato, and E. Upfal, TRIÈST: Counting Local and Global Triangles in Fully-Dynamic
        Streams with Fixed Memory Size, KDD'16.'

        The algorithm provides an estimate of the number of triangles in a graph in a streaming environment,
        where the stream represent a series of edges.
    """

    @property
    def eta(self) -> float:
        return max(
            1.0,
            ((self.t - 1) * (self.t - 2)) / (self.M * (self.M - 1))
        )

    def _update_counters(self, operator: Callable[[int, int], int], edge: FrozenSet[int]) -> None:
        """
        This function updates the counters related to estimating the number of triangles. The update happens through
        the operator lambda and involves the edge and its neighbours.

        :param operator: the lambda used to update the counters
        :param edge: the edge interested in the update
        :return: nothing
        """
        common_neighbourhood: Set[int] = reduce(
            lambda a, b: a & b,
            [
                {
                    node
                    for link in self.S if vertex in link
                    for node in link if node != vertex
                }
                for vertex in edge
            ]
        )

        for vertex in common_neighbourhood:
            self.tau += self.eta
            self.tau_vertices[vertex] += self.eta

            for node in edge:
                self.tau_vertices[node] += self.eta

    def _sample_edge(self, t: int) -> bool:
        """
        This function determines if the new edge can be inserted in memory. If yes and if the memory if full,
        the function proceeds to remove a random edge from the memory to make space.

        :param edge: the current sample under consideration
        :param t: the number of observed samples in the stream
        :return: true if the new edge can be inserted in the memory, false otherwise
        """

        if t <= self.M:
            return True
        elif bernoulli.rvs(p=self.M / t):
            edge_to_remove: FrozenSet[int] = random.choice(list(self.S))
            self.S.remove(edge_to_remove)
            return True
        else:
            return False

    def run(self) -> float:
        """
        Runs the algorithm from the stream on the file.

        :return: the estimated number of triangles
        """

        if self.verbose:
            print("Running the algorithm with M = {}.".format(self.M))

        with open(self.file, 'r') as f:
            if self.verbose:
                print("File opened, processing the stream...")

            for line in f:
                edge = _get_edge(line)
                self.t += 1

                if self.verbose and self.t % 1000 == 0:
                    print("Currently sampling element {} in the stream.".format(self.t))

                self._update_counters(lambda x, y: x + y, edge)

                if self._sample_edge(self.t):
                    self.S.add(edge)

                if self.verbose and self.t % 1000 == 0:
                    print(
                        "The current estimate for the number of triangles is {}.".format(self.tau)
                    )

            return self.tau


if __name__ == "__main__":
    TriestImproved(
        file='../data/facebook_combined.txt',
        M=1000,
        verbose=True
    ).run()
