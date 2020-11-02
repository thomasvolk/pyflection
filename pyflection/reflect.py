import inspect
import importlib
import re
from pyflection import Node, NodeProvider


def get_path(cls):
    """return full qualified class name"""
    module = cls.__module__
    name = cls.__name__
    if module is None or module == str.__class__.__module__:
        return name
    return f"{module}.{name}"


def get_class(path):
    module, class_name = path.rsplit('.', 1)
    return getattr(importlib.import_module(module), class_name)


class ClassNodeProvider(NodeProvider):
    def __init__(self, package, regexp=".+"):
        self.regexp = re.compile(regexp)
        self.package = package

    def get_relations(self, cls):
        relations = set()
        relations.update(
            [a.__class__ for a in cls.__dict__.values()
             if self.regexp.match(a.__class__.__name__)]
        )
        annotations = cls.__dict__.get('__annotations__')
        if annotations:
            relations.update(
                [a for a in annotations.values()
                 if self.regexp.match(a.__name__)]
            )
        return relations

    def find_classes(self):
        return [c[1] for c in inspect.getmembers(self.package, inspect.isclass)
                if self.regexp.match(c[0])]

    def nodes(self):
        return [
            Node(
                id=get_path(cls),
                name=cls.__name__,
                relations={get_path(c) for c in self.get_relations(cls)}
            )
            for cls in self.find_classes()
        ]


