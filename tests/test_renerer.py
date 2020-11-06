import unittest

from pyflection.reflect import ClassNodeProvider
from pyflection.render import PyVisRenderer
import spec


class ClassScannerTest(unittest.TestCase):
    PATTERN = ".+Service$|.+Broker$"
    node_provider = ClassNodeProvider(spec, PATTERN)

    def test_pyvis(self):
        nodes = self.node_provider.nodes()
        r = PyVisRenderer()
        r.render(nodes, 'test_pyvis.html')

