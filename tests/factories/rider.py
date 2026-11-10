import factory
from factory import Faker, Sequence

from uber.models import Rider


class RiderFactory(factory.Factory):
    class Meta:
        model = Rider

    first_name = Faker("first_name")
    last_name = Faker("last_name")
    email = Sequence(lambda n: f"rider{n}@example.com")
