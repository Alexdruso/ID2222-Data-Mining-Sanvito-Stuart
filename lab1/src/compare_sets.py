def compare_sets(A: set[int], B: set[int]) -> float:
    return len(A & B) / len(A | B)
