from typing import Set

import numpy as np


def min_hash(A: Set[int], hash_len: int = 100, seed: int = 0) -> np.ndarray:
    generator = np.random.default_rng(seed=seed)
    min_value = -2 ** 31
    max_value = 2 ** 31 - 1

    hash_parameters = generator.choice(
        a=generator.integers(
            low=min_value,
            high=max_value,
            size=hash_len * 2
        ),
        size=(hash_len, 2),
        replace=False
    )

    return np.asarray(
        [
            min(
                map(
                    lambda x: (x * parameters[0] + parameters[1]) % max_value,
                    A
                )
            )
            for parameters in hash_parameters
        ]
    )


if __name__ == "__main__":
    print(min_hash({1, 2, 3}))
