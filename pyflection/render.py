

class Renderer:
    def render(self, nodes, file_name):
        pass


class PyVisRenderer(Renderer):
    def render(self, nodes, file_name):
        from pyvis import network as net
        n = net.Network(notebook=True, directed=True)
        for node in nodes:
            n.add_node(node.id, label=node.name)
        for node in nodes:
            for r in node.relations:
                n.add_edge(source=node.id, to=r)
        n.write_html(file_name)