import factory
from factory.fuzzy import FuzzyChoice
from service.models import Product

class ProductFactory(factory.Factory):
    """Factory for creating fake products for testing"""

    class Meta:
        model = Product

    # If the Product model auto-generates the 'id', you can omit this.
    name = factory.Faker("word")
    description = factory.Faker("sentence", nb_words=10)
    price = factory.Faker("pyfloat", left_digits=2, right_digits=2, positive=True, min_value=1.0, max_value=1000.0)
    available = FuzzyChoice(choices=[True, False])
    category = factory.Faker("word")
