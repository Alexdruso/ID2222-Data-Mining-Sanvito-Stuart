from collections import defaultdict, Counter
from typing import Dict, List, Set, KeysView, FrozenSet
from itertools import combinations
import numpy as np


def read_dataset(
        file: str
) -> List[Set[int]]:
    """
    This function reads from a file .dat assuming that on every row of the file there is a basket of items and returns
    the list of the baskets.

    :param file: the path to the input file
    :return: the list of baskets
    """

    with open(file, "r") as f:
        baskets: List[Set[int]] = list(
            map(
                lambda basket: {int(item_id) for item_id in basket.split()},
                f.read().splitlines()
            )
        )
    f.close()

    return baskets


def find_frequent_singletons(
        baskets: List[Set[int]],
        s: int = 1,
        verbose: bool = False,
) -> Dict[FrozenSet[int], int]:
    """
    This function finds all the items having a support greater than s across all the baskets.

    :param verbose: if set to true, prints information on the process
    :param baskets: the list of all baskets represented as sets
    :param s: the threshold support to consider an item as frequent
    :return: the set of all frequent singletons
    """

    item_to_support = defaultdict(int)

    for basket in baskets:
        for item in basket:
            item_to_support[frozenset([item])] += 1

    if verbose:
        print(
            f'The market contains {len(item_to_support)} different items.'
        )
        print(
            f'The average support is {np.mean(list(item_to_support.values())):.2f}'
        )

    return dict(
        filter(
            lambda element: element[1] > s,
            item_to_support.items()
        )
    )


def generate_candidate_item_sets(
        precedent_item_sets: KeysView[FrozenSet[int]],
        item_set_length: int
) -> Set[FrozenSet[int]]:
    """
    This function returns the set of candidate new frequent itemsets for step k+1 of the a priori algorithm
    by combining the itemsets found at step k.

    :param precedent_item_sets: the frequent itemsets found at time k of the algorithm
    :param item_set_length: the length of the next candidates to be returned
    :return: a set of candidate frequent itemsets of length k+1
    """
    return {
        item_set_left | item_set_right
        for item_set_left in precedent_item_sets
        for item_set_right in precedent_item_sets
        if len(item_set_left | item_set_right) == item_set_length
    }


def filter_frequent_item_sets(
        baskets: List[Set[int]],
        candidate_item_sets: Set[FrozenSet[int]],
        item_set_length: int,
        s: int = 1
) -> Dict[FrozenSet[int], int]:
    """
    This function finds all the itemsets having a support greater than s across all the baskets.

    :param baskets: the list of all baskets represented as sets
    :param candidate_item_sets: the set of itemsets candidate to be frequent
    :param item_set_length: the length of the itemsets
    :param s: the threshold support to consider an itemset as frequent
    :return: the set of all frequent itemsets
    """
    item_set_to_support = Counter(
        [
            frozenset(item_set)
            for basket in baskets
            for item_set in combinations(basket, item_set_length)
            if frozenset(item_set) in candidate_item_sets
        ]
    )

    return dict(
        filter(
            lambda element: element[1] > s,
            item_set_to_support.items()
        )
    )


def find_frequent_item_sets(
        file: str,
        s: int = 1,
        verbose: bool = False,
) -> Dict[FrozenSet[int], int]:
    """
    This function reads from a file .dat assuming that on every row of the file there is a basket of items.
    The function then generates the set of frequent itemsets having support greater or equal than s and maximum size
    equal to maximum_item_set_size with the apriori algorithm.

    :param verbose:  if set to true, prints information on the process
    :param file: the path to the input file
    :param s: the minimum support required to consider an itemset frequent
    :return: the set of all frequent itemsets, represented as frozensets, mapped to their support
    """

    baskets = read_dataset(file=file)

    # The first frequent itemsets are the frequent singletons themselves
    frequent_item_sets: Dict[FrozenSet[int], int] = find_frequent_singletons(
        baskets=baskets, s=s, verbose=verbose)

    if verbose:
        print(
            f'The most frequent singletons have been calculated. {len(frequent_item_sets)} singletons was/were found.'
        )

    precedent_frequent_item_sets = frequent_item_sets.keys()
    item_set_length = 2
    while len(precedent_frequent_item_sets) > 1:
        if verbose:
            print(
                "Computing frequent itemsets of length {}...".format(item_set_length)
            )

        candidate_item_sets = generate_candidate_item_sets(
            precedent_item_sets=precedent_frequent_item_sets,
            item_set_length=item_set_length
        )

        if verbose:
            print(
                "{} candidates generated!".format(len(candidate_item_sets))
            )

        if len(candidate_item_sets) > 0:
            new_frequent_item_sets = filter_frequent_item_sets(
                baskets=baskets,
                candidate_item_sets=candidate_item_sets,
                item_set_length=item_set_length,
                s=s
            )

            frequent_item_sets.update(new_frequent_item_sets)
            precedent_frequent_item_sets = new_frequent_item_sets.keys()
            item_set_length += 1

            if verbose:
                print(
                    f'Done! {len(new_frequent_item_sets)} frequent items was/were found.'
                )

    if verbose:
        print(
            f'\nIn total {len(frequent_item_sets)} frequent items were found.'
        )

    return frequent_item_sets


if __name__ == "__main__":
    print(
        find_frequent_item_sets(
            file='../data/T10I4D100K.dat',
            s=1000
        )
    )
