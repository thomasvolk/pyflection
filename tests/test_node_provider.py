import unittest
from pyflection.reflect import ClassNodeProvider, TracingClassNodeProvider
import spec


class ClassNodeProviderTest(unittest.TestCase):
    PATTERN = ".+Service$|.+Broker$"
    node_provider = ClassNodeProvider(spec, PATTERN)

    def test_class_list(self):
        class_names = [c.__name__ for c in self.node_provider.find_classes()]
        class_names.sort()
        self.assertEqual(
            ['ConfigurationService',
             'CustomerService',
             'EmailService',
             'NotificationBroker',
             'NotificationService',
             'OrderService',
             'SMSService'],
            class_names
        )

    def test_relations(self):
        nodes = self.node_provider.nodes()
        self.assertEqual(7, len(nodes))
        notification_service_node = nodes[4]
        self.assertEqual("spec.NotificationService", notification_service_node.id)
        self.assertEqual(
            notification_service_node.relations,
            {'spec.CustomerService', 'spec.SMSService', 'spec.EmailService'}
        )

    def test_trace(self):
        node_provider = TracingClassNodeProvider(spec, self.PATTERN)
        node_provider.tracing_on()
        # trace the constructor call
        spec.NotificationService()
        # done
        node_provider.tracing_off()
        nodes = node_provider.nodes()
        self.assertEqual(7, len(nodes))
        notification_service_node = nodes[4]
        self.assertEqual("spec.NotificationService", notification_service_node.id)
        self.assertEqual(
            notification_service_node.relations,
            {'spec.CustomerService', 'spec.SMSService', 'spec.EmailService', 'spec.ConfigurationService'}
        )