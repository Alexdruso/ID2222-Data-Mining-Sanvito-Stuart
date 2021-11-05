import functools


class Shingling:

    def __init__(self, k: int, document: str) -> None:
        self.k = k
        self.document = document

    @functools.lru_cache()
    def shinglings(self) -> set:
        result = set()
        document_length = len(self.document)

        for start in range(document_length - self.k):
            result.add(self.document[start:start + self.k].__hash__())

        return result
