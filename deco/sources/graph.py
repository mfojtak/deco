from graphviz import Digraph
import pathlib
import inspect

class Graph:
    def __init__(self, nodes):
        self._nodes = set()
        self._inputs = []
        self._outputs = []
        for node in nodes:
            self._walk(node)
        for item in self._nodes:
            if len(item._inputs) == 0:
                self._inputs.append(item)
            if len(item._outputs) == 0:
                self._outputs.append(item)
        for i, node in enumerate(self._nodes):
            node._id = i

    def inputs(self):
        return self._inputs
    def outputs(self):
        return self._outputs
    def nodes(self):
        return list(self._nodes)

    def _walk(self, node):
        self._nodes.add(node)
        for child in node._inputs:
            self._walk(child)
    
    def _name(self, node):
        name = "{}_{}".format(node.__class__.__name__, node._id)
        return name
    
    def dot(self):
        g = Digraph(node_attr={'shape': 'Mrecord'})
        groups = {}
        rest =[]

        for node in self._nodes:
            properties = inspect.getmembers(type(node), lambda o: isinstance(o, property))
            label = "{" + self._name(node)
            for name, _ in properties:
                value = getattr(node, name)
                label += "|{}:{}".format(name, value)
            label += "}"
            g.node(self._name(node), label)
            for inp in node._inputs:
                if hasattr(node, "_group") and hasattr(inp, "_group") and inp._group == node._group:
                    group = "cluster_{}".format(node._group)
                    if group not in groups.keys():
                        groups[group] = []
                    groups[group].append((self._name(inp), self._name(node)))
                else:
                    rest.append((self._name(inp), self._name(node)))
        for group in groups.keys():
            with g.subgraph(name=group) as a:
                a.edges(groups[group])
                a.attr(label=group)
        g.edges(rest)
        return g
    
    def render(self, filename):
        g = self.dot()
        p = pathlib.Path(filename)
        g.format = p.suffix.split(".")[-1]
        g.filename = p.with_suffix('')
        g.render()

        
