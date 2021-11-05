import functools


@functools.lru_cache()
def shinglings(document: str, k: int) -> set:
    result = set()
    document_length = len(document)

    for start in range(document_length - k):
        result.add(document[start:start + k].__hash__())

    return result
