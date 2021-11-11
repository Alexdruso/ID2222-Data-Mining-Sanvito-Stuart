import numpy as np


def compare_signatures(A: np.ndarray, B: np.ndarray) -> float:
    """
    Estimates the Jaccard similarity between A and B as the probability to have an equal entry in the signatures of A
    and B.
    :param A: the minhashed representation of document A
    :param B: the minhashed representation of document A
    :return: an estimate of the Jaccard similarity between A and B
    """
    return sum(A == B) / len(A)
