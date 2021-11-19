from typing import Tuple, Dict, List, Set


def generate_rules(
        frequent_item_sets: Dict[Set[int], int],
        s: int = 1,
        c: float = 0.1
) -> Dict[Set[int], Set[Set[int]]]:
    """
    This function returns all the association rules having support greater than s and confidence greater than c.

    :param frequent_item_sets: the dictionary of all frequent itemsets with their respective support
    :param s: the threshold support
    :param c: the threshold confidence
    :return: a dictionary linking each left side itemset of the association rule with all the right side itemsets
    """
