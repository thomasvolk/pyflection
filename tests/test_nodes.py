import unittest
from pyflection import merge_nodes, Node


class ClassScannerTest(unittest.TestCase):
    def test_merge_nodes(self):
        one_node_a = [Node(id="node", name="node", relations={"a", "b"})]
        one_node_b = [Node(id="node", name="node", relations={"c", "b"})]
        two_nodes = [Node(id="node", name="node", relations={"c", "d"}),
                     Node(id="node2", name="node2", relations={"c", "b"})]

        merged_noes = merge_nodes(one_node_a, one_node_b, two_nodes)
        self.assertEqual([
            Node(id="node", name="node", relations={"a", "b", "c", "d"}),
            Node(id="node2", name="node2", relations={"c", "b"})
        ], merged_noes)
