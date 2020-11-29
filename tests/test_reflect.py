import unittest
from pyflection.reflect import TracingClassNodeProvider, ClassNodeProvider, get_path, get_class
import spec


class ClassScannerTest(unittest.TestCase):
    PATTERN = "Notification.+$"
    node_provider = ClassNodeProvider(spec, PATTERN)

    def test_find_classes(self):
        classes = self.node_provider.find_classes()
        self.assertEqual(
            [spec.NotificationBroker,
             spec.NotificationService
             ],
            classes
        )

    def test_relation(self):
        relations = self.node_provider.get_relations_from_class(spec.NotificationBroker)
        self.assertEqual({spec.NotificationService}, relations)

    def test_get_path(self):
        self.assertEqual('pyflection.reflect.ClassNodeProvider', get_path(ClassNodeProvider))

    def test_get_class(self):
        self.assertEqual(ClassNodeProvider, get_class('pyflection.reflect.ClassNodeProvider'))

    def test_trace(self):
        node_provider = TracingClassNodeProvider(spec, self.PATTERN)
        node_provider.tracing_on()
        spec.NotificationService()
        node_provider.tracing_off()
        node_provider.nodes()
