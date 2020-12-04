import unittest
import matplotlib.pyplot as plt
from pyflection.reflect import ClassNodeProvider
from pyflection.export import NetworkXExport
import networkx as nx
import spec


class ExportTest(unittest.TestCase):
    PATTERN = ".+Service$|.+Broker$"
    node_provider = ClassNodeProvider(spec, PATTERN)

    def test_networkx(self):
        nodes = self.node_provider.nodes()
        e = NetworkXExport()
        graph = e.export(nodes)
        self.assertEqual(7, len(graph.nodes))
        ax = plt.subplot(111)
        ax.set_title('test_networkx', fontsize=10)

        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, node_size=9000, node_color='steelblue', node_shape='h',
                font_color='black', with_labels=True, font_size=6, font_weight='bold')

        plt.tight_layout()
        plt.show()
        plt.savefig("export_test_networkx.png", format="PNG")


