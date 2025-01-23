import factory
from factory.fuzzy import FuzzyChoice
from service.models import Product

class ProductFactory(factory.Factory):
    """Factory for creating fake products for testing"""

    class Meta:
        model = Product

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("word")
    description = factory.Faker("sentence", nb_words=10)
    price = factory.Faker("pyfloat", left_digits=2, right_digits=2, positive=True)
    available = FuzzyChoice(choices=[True, False])
    category = factory.Faker("word")
