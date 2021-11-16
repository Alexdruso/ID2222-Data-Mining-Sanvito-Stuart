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

    precedent_frequent_item_sets = frequent_singletons.keys()
    for _ in range(1, largest_item_set_size + 1):
        print('kek')

    return frequent_item_sets


if __name__ == "__main__":
    print(
        find_frequent_item_sets(file='../data/T10I4D100K.dat', s=10)
    )
