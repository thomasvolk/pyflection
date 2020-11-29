

class Export:
    def export(self, nodes):
        pass


class NetworkXExport(Export):
    def export(self, nodes):
        import networkx as nx
        graph = nx.Graph()
        for node in nodes:
            graph.add_node(node.id, label=node.name, title=node.name)
        for node in nodes:
            for r in node.relations:
                graph.add_edge(node.id, r)
        return graph
