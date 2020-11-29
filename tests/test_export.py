import unittest

from pyflection.reflect import ClassNodeProvider
from pyflection.export import NetworkXExport
import spec


class ClassScannerTest(unittest.TestCase):
    PATTERN = ".+Service$|.+Broker$"
    node_provider = ClassNodeProvider(spec, PATTERN)

    def test_networkx(self):
        nodes = self.node_provider.nodes()
        e = NetworkXExport()
        graph = e.export(nodes)
        self.assertEqual(7, len(graph.nodes))

