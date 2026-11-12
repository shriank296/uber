import random

from factory.base import Factory
from factory.declarations import LazyFunction
from factory.faker import Faker

from uber.models import Driver
from uber.models.enums import DriverStatus


class DriverFactory(Factory[Driver]):
    class Meta:
        model = Driver

    first_name = Faker("first_name")
    last_name = Faker("last_name")
    status = LazyFunction(lambda: random.choice(list(DriverStatus)))
    latitude = Faker("latitude")
    longitude = Faker("longitude")
