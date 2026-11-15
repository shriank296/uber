import random

from factory.base import Factory
from factory.declarations import LazyFunction, SubFactory
from factory.faker import Faker

from tests.factories.driver import DriverFactory
from tests.factories.rider import RiderFactory
from uber.models import Ride
from uber.models.enums import RideStatus


class RideFactory(Factory[Ride]):
    class Meta:
        model = Ride

    rider = SubFactory(RiderFactory)
    driver = SubFactory(DriverFactory)
    pickup_latitude = Faker("latitude")
    pickup_longitude = Faker("longitude")
    drop_latitude = Faker("latitude")
    drop_longitude = Faker("longitude")
    status = LazyFunction(lambda: random.choice(list(RideStatus)))
