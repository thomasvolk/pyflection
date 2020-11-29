import inspect
import importlib
import re
from pyflection import Node, NodeProvider
import sys


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


class ReflectionNodeProvider(NodeProvider):
    def __init__(self, package, regexp):
        self.regexp = re.compile(regexp)
        self.package = package


class ClassNodeProvider(ReflectionNodeProvider):
    def get_relations_from_class(self, cls):
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
                relations={get_path(c) for c in self.get_relations_from_class(cls)}
            )
            for cls in self.find_classes()
        ]


class TracingClassNodeProvider(ReflectionNodeProvider):
    def __init__(self, package, regexp):
        super(TracingClassNodeProvider, self).__init__(package, regexp)
        self.objects = []

    def get_relations_from_object(self, obj):
        relations = set()
        relations.update([
            m.__class__ for m in obj.__dict__.values()
            if isinstance(m, object) and self.regexp.match(m.__class__.__name__)
        ])
        return relations

    def __trace(self, frame, msg, arg):
        local_objects = [o for o in frame.f_locals.values() if isinstance(o, object)]
        self.objects.extend([o for o in local_objects if self.regexp.match(o.__class__.__name__)])

    def tracing_on(self):
        sys.settrace(self.__trace)

    def tracing_off(self):
        sys.settrace(None)

    def nodes(self):
        return [
            Node(
                id=get_path(o.__class__),
                name=o.__class__.__name__,
                relations={get_path(c) for c in self.get_relations_from_object(o)}
            )
            for o in self.objects
        ]
