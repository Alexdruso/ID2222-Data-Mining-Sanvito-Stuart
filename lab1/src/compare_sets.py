from typing import Set


def compare_sets(A: Set[int], B: Set[int]) -> float:
    return len(A & B) / len(A | B)
