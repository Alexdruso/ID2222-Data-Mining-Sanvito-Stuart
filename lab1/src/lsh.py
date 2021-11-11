from math import ceil
from typing import Tuple, Dict, Set

import numpy as np

from compare_signatures import compare_signatures

from itertools import combinations


def hash_band(band: np.ndarray) -> np.ndarray:
    """
    This function might be changed later to improve performance. It is meant to hash the band of each document.
    :param band: the matrix of shape (band_length, documents_number)
    :return: an array of shape (1, documents_number) containing the hashed band for each document
    """
    return np.sum(a=band, axis=0)


def lsh(M: np.ndarray, t: float, b: int = 1) -> Set[Tuple[int, int]]:
    """
    This function takes as input the minhash signatures of M.shape[1] documents and returns all the pairs of documents
    with estimated similarity larger than t.
    :param M: matrix having as columns the signatures of the documents
    :param t: threshold for the similarity
    :param b: number of bands
    :return: the pairs of indices of documents with estimated similarity larger than t
    """
    candidates: Set[Tuple[int, int]] = set()
    hash_length: int = len(M)
    documents_number: int = M.shape[1]
    band_length: int = ceil(hash_length / b)

    for band_index in range(0, hash_length, band_length):
        collision_hashmap: Dict[int, Set[int]] = {}

        # shape (band_length, documents_number)
        band = M[band_index: min(band_index + band_length, hash_length), :]

        # shape (1, documents_number)
        hashed_band = hash_band(band=band)

        for document_index in range(documents_number):
            document_band_hash = hashed_band[document_index]

            if document_band_hash in collision_hashmap:
                collision_hashmap[document_band_hash].add(document_index)
            else:
                collision_hashmap[document_band_hash] = {document_index}

        for collision_set in collision_hashmap.values():
            candidates.update(set(combinations(collision_set, 2)))

    return set(
        filter(
            lambda pair: compare_signatures(M[:, pair[0]], M[:, pair[1]]) >= t,
            candidates
        )
    )


if __name__ == "__main__":
    M = np.ones(shape=(100, 10))
    print(lsh(M, 1, 10))
