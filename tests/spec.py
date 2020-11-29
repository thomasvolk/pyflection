from dataclasses import dataclass
from typing import List
from pyflection.utils import Borg


@dataclass
class Customer:
    id: str
    email: str
    phone_number: str


@dataclass
class Notification:
    customer_id: str
    message: str


@dataclass
class Order:
    customer_id: str
    items: List[str]


class EventBrokerSupport(Borg):
    def publish(self, message):
        pass


class ConfigurationService:
    pass


class CustomerService:
    configuration: ConfigurationService

    def get_customer(self, customer_id) -> Customer:
        pass


class SMSService:
    def send_sms(self, number, message):
        pass


class EmailService:
    def send_email(self, email, message):
        pass


class NotificationService:
    customer_service = CustomerService()
    email_service = EmailService()
    sms_service = SMSService()

    def __init__(self):
        self.configuration = ConfigurationService()

    def send(self, notification: Notification):
        customer = self.customer_service.get_customer(notification.customer_id)
        self.email_service.send_email(customer.email, notification.message)


class NotificationBroker(EventBrokerSupport):
    notification_service = NotificationService()

    def publish(self, notification):
        self.notification_service.send(notification)


class OrderService:
    configuration: ConfigurationService
    notification_broker = NotificationBroker()

    def take_order(self, order: Order):
        self.notification_broker.publish(Notification(order.customer_id, "order received"))
