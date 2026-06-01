from abc import ABC, abstractmethod
from typing import Any


class ASTParser(ABC):
    @abstractmethod
    def parse(self, code: str) -> dict[str, Any]:
        raise NotImplementedError
