import numpy as np


def compare_signatures(A: np.ndarray, B: np.ndarray) -> float:
    return sum(A == B) / len(A)
