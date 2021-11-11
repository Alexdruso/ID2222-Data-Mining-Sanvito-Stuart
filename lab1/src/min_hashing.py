from typing import Set

import numpy as np


def min_hash(A: Set[int], hash_length: int = 100, seed: int = 0) -> np.ndarray:
    """
    The function takes as input the set of hashed shingling in a document and returns a vector representation of the
    document hashed through min hashing.
    :param A: the set of hashed shingling representing a document
    :param hash_length: the length of the signature to be returned
    :param seed: the seed used to generate the hash functions
    :return: a vector representation of the document, with len=hash_len
    """
    generator = np.random.default_rng(seed=seed)
    min_value = -2 ** 31
    max_value = 2 ** 31 - 1

    hash_parameters = generator.choice(
        a=generator.integers(
            low=min_value,
            high=max_value,
            size=hash_length * 2
        ),
        size=(hash_length, 2),
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
