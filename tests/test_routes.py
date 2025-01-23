

"""
Test cases for Product Model

Test cases can be run with:
    nosetests
    coverage report -m

While debugging just these tests it's convenient to use this:
    nosetests --stop tests/test_models.py:TestProductModel

"""
import os
import logging
import unittest
from decimal import Decimal
from service.models import Product, Category, db
from service import app
from tests.factories import ProductFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)


######################################################################
#  P R O D U C T   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestProductModel(unittest.TestCase):
    """Test Cases for Product Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Product.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Product).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_product(self):
        """It should Create a product and assert that it exists"""
        product = Product(name="Fedora", description="A red hat", price=12.50, available=True, category=Category.CLOTHS)
        self.assertEqual(str(product), "<Product Fedora id=[None]>")
        self.assertTrue(product is not None)
        self.assertEqual(product.id, None)
        self.assertEqual(product.name, "Fedora")
        self.assertEqual(product.description, "A red hat")
        self.assertEqual(product.available, True)
        self.assertEqual(product.price, 12.50)
        self.assertEqual(product.category, Category.CLOTHS)

    def test_add_a_product(self):
        """It should Create a product and add it to the database"""
        products = Product.all()
        self.assertEqual(products, [])
        product = ProductFactory()
        product.id = None
        product.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(product.id)
        products = Product.all()
        self.assertEqual(len(products), 1)
        # Check that it matches the original product
        new_product = products[0]
        self.assertEqual(new_product.name, product.name)
        self.assertEqual(new_product.description, product.description)
        self.assertEqual(Decimal(new_product.price), product.price)
        self.assertEqual(new_product.available, product.available)
        self.assertEqual(new_product.category, product.category)

    #
    # ADD YOUR TEST CASES HERE
    #
    def test_list_products(client):
        """Test retrieving all products"""
        response = client.get("/products")
        assert response.status_code == 200

    def test_get_product(client, product):
        """Test retrieving a single product by ID"""
        response = client.get(f"/products/{product.id}")
        assert response.status_code == 200
        assert response.json["id"] == product.id

    def test_create_product(client):
        """Test creating a new product"""
        new_product = {
            "name": "Test Product",
            "description": "Test description",
            "price": 19.99,
            "available": True,
            "category": "Test Category"
        }
        response = client.post("/products", json=new_product)
        assert response.status_code == 201
        assert response.json["name"] == "Test Product"

    def test_update_product(client, product):
        """Test updating an existing product"""
        updated_data = {"name": "Updated Product"}
        response = client.put(f"/products/{product.id}", json=updated_data)
        assert response.status_code == 200
        assert response.json["name"] == "Updated Product"

    def test_delete_product(client, product):
        """Test deleting a product"""
        response = client.delete(f"/products/{product.id}")
        assert response.status_code == 204


    def test_list_products_by_name(client):
        """Test retrieving products by name"""
        # Create a product for testing
        product = ProductFactory(name="Test Product")
        product.create()

        # Make a GET request to search for the product by name
        response = client.get("/products", query_string={"name": "Test Product"})
        
        assert response.status_code == 200
        assert len(response.json) > 0  # Ensure that the product is in the response
        assert response.json[0]["name"] == "Test Product"  # Ensure the name matches

    def test_list_products_by_category(client):
        """Test retrieving products by category"""
        # Create products for testing
        product1 = ProductFactory(category="Electronics")
        product1.create()
        product2 = ProductFactory(category="Electronics")
        product2.create()
        product3 = ProductFactory(category="Clothing")
        product3.create()

        # Make a GET request to search for products by category "Electronics"
        response = client.get("/products", query_string={"category": "Electronics"})
        
        assert response.status_code == 200
        assert len(response.json) == 2  # Expecting two products in the "Electronics" category
        for product in response.json:
            assert product["category"] == "Electronics"  # Ensure the category is Electronics

    def test_list_products_by_availability(client):
        """Test retrieving products by availability"""
        # Create products for testing
        product1 = ProductFactory(available=True)
        product1.create()
        product2 = ProductFactory(available=True)
        product2.create()
        product3 = ProductFactory(available=False)
        product3.create()

        # Make a GET request to search for available products (available=True)
        response = client.get("/products", query_string={"available": "true"})
        
        assert response.status_code == 200
        assert len(response.json) == 2  # Expecting two products that are available
        for product in response.json:
            assert product["available"] is True  # Ensure the availability is True

        # Make a GET request to search for unavailable products (available=False)
        response = client.get("/products", query_string={"available": "false"})
        
        assert response.status_code == 200
        assert len(response.json) == 1  # Expecting one product that is unavailable
        for product in response.json:
            assert product["available"] is False  # Ensure the availability is False
