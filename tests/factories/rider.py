from factory.base import Factory
from factory.declarations import Sequence
from factory.faker import Faker

from uber.models import Rider


class RiderFactory(Factory[Rider]):
    class Meta:
        model = Rider

    first_name = Faker("first_name")
    last_name = Faker("last_name")
    email = Sequence(lambda n: f"rider{n}@example.com")
