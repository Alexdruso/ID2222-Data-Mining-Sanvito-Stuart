import functools
from typing import Set


class Shingling:

    def __init__(self) -> None:
        self._shingling_to_int = dict()
        self._shingling_number = 0
        super().__init__()

    def hash(self, shingling: str) -> int:
        if shingling in self._shingling_to_int:
            return self._shingling_to_int[shingling]
        else:
            self._shingling_to_int[shingling] = self._shingling_number
            self._shingling_number += 1
            return self._shingling_number - 1

    @functools.lru_cache()
    def shingling(self, document: str, k: int) -> Set[int]:
        result = set()
        document_length = len(document)

        for start in range(document_length - k):
            result.add(self.hash(document[start:start + k]))

        return result
