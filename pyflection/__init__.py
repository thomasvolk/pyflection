from dataclasses import dataclass, field
from typing import Set, List, Mapping


class NodeProvider:
    def nodes(self):
        pass


@dataclass(frozen=True, eq=True, repr=True)
class Node:
    id: str
    name: str = field(hash=False)
    relations: Set[str] = field(hash=False)


def merge_nodes(*list_of_node_list: List[Node]):
    nodes_dict: Mapping[str, Node] = {}
    for node_list in list_of_node_list:
        for node in node_list:
            dict_node = nodes_dict.get(node.id)
            if dict_node:
                dict_node.relations.update(node.relations)
            else:
                nodes_dict[node.id] = node
    return list(nodes_dict.values())
