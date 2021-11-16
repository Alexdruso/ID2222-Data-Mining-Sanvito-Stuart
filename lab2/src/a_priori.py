from typing import Tuple, Dict


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

    with open(file, "r") as f:
        baskets = list(
            map(
                lambda basket: {int(item_id) for item_id in basket.split()},
                f.read().splitlines()
            )
        )
    f.close()

    largest_item_set_size = max(
        map(
            len,
            baskets
        )
    )

    return frequent_item_sets

if __name__ == "__main__":
    print(
        find_frequent_item_sets(file='../data/T10I4D100K.dat', s=10)
    )
