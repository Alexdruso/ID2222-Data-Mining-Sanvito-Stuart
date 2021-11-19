from collections import defaultdict
from typing import Dict, List, Set, KeysView


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
        s: int = 1
) -> Dict[Set[int], int]:
    """
    This function finds all the items having a support greater than s across all the baskets.

    :param baskets: the list of all baskets represented as sets
    :param s: the threshold support to consider an item as frequent
    :return: the set of all frequent singletons
    """

    item_to_support = defaultdict(int)

    for basket in baskets:
        for item in basket:
            item_to_support[frozenset([item])] += 1

    return dict(
        filter(
            lambda element: element[1] > s,
            item_to_support.items()
        )
    )


def generate_candidate_item_sets(
        precedent_item_sets: KeysView[Set[int]],
        item_set_length: int
) -> Set[Set[int]]:
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
        candidate_item_sets: Set[Set[int]],
        s: int = 1
) -> Dict[Set[int], int]:
    item_set_to_support = {
        candidate_item_set: sum(map(lambda basket: candidate_item_set.issubset(basket), baskets))
        for candidate_item_set in candidate_item_sets
    }

    return dict(
        filter(
            lambda element: element[1] > s,
            item_set_to_support.items()
        )
    )


def find_frequent_item_sets(
        file: str,
        s: int = 1
) -> Dict[Set[int], int]:
    """
    This function reads from a file .dat assuming that on every row of the file there is a basket of items.
    The function then generates the set of frequent itemsets having support greater or equal than s and maximum size
    equal to maximum_item_set_size with the apriori algorithm.

    :param file: the path to the input file
    :param s: the minimum support required to consider an itemset frequent
    :return: the set of all frequent itemsets, represented as frozensets, mapped to their support
    """

    baskets = read_dataset(file=file)

    # The first frequent itemsets are the frequent singletons themselves
    frequent_item_sets: Dict[Set[int], int] = find_frequent_singletons(baskets=baskets, s=s)

    print("The most frequent singletons have been calculated.")

    precedent_frequent_item_sets = frequent_item_sets.keys()
    item_set_length = 2
    while len(precedent_frequent_item_sets) > 1:
        print("Computing frequent itemsets of length {}...".format(item_set_length))

        candidate_item_sets = generate_candidate_item_sets(
            precedent_item_sets=precedent_frequent_item_sets,
            item_set_length=item_set_length
        )

        print("Candidates generated!")

        new_frequent_item_sets = filter_frequent_item_sets(
            baskets=baskets,
            candidate_item_sets=candidate_item_sets,
            s=s
        )

        frequent_item_sets.update(new_frequent_item_sets)
        precedent_frequent_item_sets = new_frequent_item_sets.keys()
        item_set_length += 1

        print("Done!")

    return frequent_item_sets


if __name__ == "__main__":
    print(
        find_frequent_item_sets(
            file='../data/T10I4D100K.dat',
            s=1
        )
    )
