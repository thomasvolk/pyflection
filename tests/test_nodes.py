import unittest
from pyflection.reflect import ClassNodeProvider
import spec


class ClassScannerTest(unittest.TestCase):
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
        notification_service = self.node_provider.nodes()[4]
        self.assertEqual(
            notification_service.relations,
            {'spec.CustomerService', 'spec.SMSService', 'spec.EmailService'}
        )

