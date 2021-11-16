from typing import Tuple, Dict, List, Set
from collections import defaultdict


def read_dataset(file: str) -> Tuple[List[Set[int]], int]:
    """
    This function reads from a file .dat assuming that on every row of the file there is a basket of items and returns
    the list of the baskets and the maximum basket size.

    :param file: the path to the input file
    :return: a tuple containing the list of baskets and the maximum basket size
    """

    with open(file, "r") as f:
        baskets: List[Set[int]] = list(
            map(
                lambda basket: {int(item_id) for item_id in basket.split()},
                f.read().splitlines()
            )
        )
    f.close()

    largest_item_set_size: int = max(
        map(
            len,
            baskets
        )
    )

    return baskets, largest_item_set_size


def find_frequent_singletons(baskets: List[Set[int]], s: int = 1) -> Dict[Tuple[int], int]:
    """
    This function finds all the items having a support greater than s across all the baskets.

    :param baskets: the list of all baskets represented as sets
    :param s: the threshold support to consider an item as frequent
    :return: the set of all frequent singletons
    """

    item_to_support = defaultdict(int)

    for basket in baskets:
        for item in basket:
            item_to_support[(item,)] += 1

    return dict(
        filter(
            lambda element: element[1] > s,
            item_to_support.items()
        )
    )


def generate_candidate_item_sets(
        precedent_item_sets: Set[Tuple[int, ...]],
        frequent_singletons: Set[Tuple[int]]
) -> Set[Tuple[int, ...]]:
    """
    This function returns the set of candidate new frequent itemsets for step k+1 of the a priori algorithm
     by combining the itemsets found at step k of the algorithm with frequent singletons.

    :param precedent_item_sets: the frequent itemsets found at time k of the algorithm
    :param frequent_singletons: the frequent singletons in the dataset
    :return: a set of candidate frequent itemsets of length k+1
    """
    return {
        item_set + singleton
        for item_set in precedent_item_sets
        for singleton in frequent_singletons
        if singleton not in item_set
    }


def find_frequent_item_sets(file: str, s: int = 1) -> Dict[Tuple[int, ...], int]:
    """
    This function reads from a file .dat assuming that on every row of the file there is a basket of items.
    The function then generates the set of frequent itemsets having support greater or equal than s with the apriori
    algorithm.

    :param file: the path to the input file
    :param s: the minimum support required to consider an itemset frequent
    :return: the set of all frequent itemsets, represented as tuples, mapped to their support
    """

    frequent_item_sets: Dict[Tuple[int, ...], int] = {}

    baskets, largest_item_set_size = read_dataset(file=file)

    frequent_singletons = find_frequent_singletons(baskets=baskets, s=s)
    frequent_item_sets.update(frequent_singletons)
    frequent_singletons = set(frequent_singletons.keys())

    precedent_frequent_item_sets = frequent_singletons
    for _ in range(1, largest_item_set_size + 1):
        candidate_item_sets = generate_candidate_item_sets(
            precedent_item_sets=precedent_frequent_item_sets,
            frequent_singletons=frequent_singletons
        )

    return frequent_item_sets


if __name__ == "__main__":
    print(
        find_frequent_item_sets(file='../data/T10I4D100K.dat', s=10)
    )
