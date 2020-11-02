from dataclasses import dataclass, field
from typing import Set, Mapping


class NodeProvider:
    def nodes(self):
        pass


@dataclass(frozen=True, eq=True, repr=True)
class Node:
    id: str
    name: str = field(hash=False)
    relations: Set[str] = field(hash=False)