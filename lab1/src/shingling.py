import functools
from typing import Set


@functools.lru_cache()
def shingling(document: str, k: int) -> Set[int]:
    result = set()
    document_length = len(document)

    for start in range(document_length - k):
        result.add(document[start:start + k].__hash__())

    return result
