from typing import Set


def compare_sets(A: Set[int], B: Set[int]) -> float:
    """
    This function computes the Jaccard similarity between sets A and B.
    :param A: set of hashed shingling in document A
    :param B: set of hashed shingling in document B
    :return: the Jaccard similarity between A and B
    """
    return len(A & B) / len(A | B)
