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

    def test_create_a_product(self):
        """It should Create a product and assert that it exists"""
        product = Product(name="Fedora", description="A red hat", price=12.50, available=True, category=Category.CLOTHS)
        self.assertIsNone(product.id)  # ID should be None before commit

        db.session.add(product)
        db.session.commit()

        # Check the product details in the database
        self.assertIsNotNone(product.id)  # ID should not be None after commit
        self.assertEqual(product.name, "Fedora")
        self.assertEqual(product.description, "A red hat")
        self.assertEqual(product.price, 12.50)
        self.assertEqual(product.available, True)
        self.assertEqual(product.category, Category.CLOTHS)

    def test_add_a_product(self):
        """It should Create a product and add it to the database"""
        products = Product.all()
        self.assertEqual(products, [])

        product = ProductFactory()  # Using ProductFactory to create a fake product
        product.create()  # Create the product in the database
       
        # Assert that the product is assigned an ID and shows up in the database
        self.assertIsNotNone(product.id)
        products = Product.all()
        self.assertEqual(len(products), 1)

        new_product = products[0]
        self.assertEqual(new_product.name, product.name)
        self.assertEqual(new_product.description, product.description)
        self.assertEqual(Decimal(new_product.price), product.price)
        self.assertEqual(new_product.available, product.available)
        self.assertEqual(new_product.category, product.category)
    # update 
    def test_update_a_product(self):
        """It should update a product's details and reflect the changes in the database"""
        
        # Create a product to be updated
        product = Product(name="Fedora", description="A red hat", price=12.50, available=True, category=Category.CLOTHS)
        db.session.add(product)
        db.session.commit()

        # Ensure the product was created and has the expected initial values
        self.assertIsNotNone(product.id)
        self.assertEqual(product.name, "Fedora")
        self.assertEqual(product.description, "A red hat")
        self.assertEqual(product.price, 12.50)
        self.assertEqual(product.available, True)
        self.assertEqual(product.category, Category.CLOTHS)

        # Update the product's details
        product.name = "Updated Fedora"
        product.description = "An updated red hat"
        product.price = 15.00
        product.available = False
        product.category = Category.ELECTRONICS
        
        db.session.commit()

        # Fetch the updated product from the database
        updated_product = Product.query.get(product.id)

        # Assert that the updated values are correctly persisted
        self.assertEqual(updated_product.name, "Updated Fedora")
        self.assertEqual(updated_product.description, "An updated red hat")
        self.assertEqual(updated_product.price, 15.00)
        self.assertEqual(updated_product.available, False)
        self.assertEqual(updated_product.category, Category.ELECTRONICS)


#delete
    def test_delete_a_product(self):
        """It should delete a product and ensure it no longer exists in the database"""

        # Create a product to be deleted
        product = Product(name="Fedora", description="A red hat", price=12.50, available=True, category=Category.CLOTHS)
        db.session.add(product)
        db.session.commit()

        # Ensure the product was created and has the expected initial values
        self.assertIsNotNone(product.id)
        self.assertEqual(product.name, "Fedora")
        
        # Get the product from the database to ensure it exists
        product_to_delete = Product.query.get(product.id)
        self.assertIsNotNone(product_to_delete)

        # Delete the product
        product_to_delete.delete()
        db.session.commit()

        # Verify the product is deleted by attempting to fetch it from the database
        deleted_product = Product.query.get(product.id)
        self.assertIsNone(deleted_product)
#list all products
    def test_list_all_products(self):
        """It should list all products in the database"""

        # Create and add some products to the database
        product1 = Product(name="Fedora", description="A red hat", price=12.50, available=True, category=Category.CLOTHS)
        product2 = Product(name="Laptop", description="A high-end laptop", price=1500.00, available=True, category=Category.ELECTRONICS)
        product3 = Product(name="Shirt", description="A cotton shirt", price=25.00, available=False, category=Category.CLOTHS)
        
        db.session.add(product1)
        db.session.add(product2)
        db.session.add(product3)
        db.session.commit()

        # List all products using the all method
        products = Product.all()

        # Assert that the correct number of products are returned
        self.assertEqual(len(products), 3)

        # Check the names of the products to ensure they match the expected ones
        product_names = [product.name for product in products]
        self.assertIn("Fedora", product_names)
        self.assertIn("Laptop", product_names)
        self.assertIn("Shirt", product_names)

        # Optionally, check other properties of the products as well
        self.assertEqual(products[0].name, "Fedora")
        self.assertEqual(products[1].name, "Laptop")
        self.assertEqual(products[2].name, "Shirt")
# find by product name
    def test_find_product_by_name(self):
        """It should find a product by its name"""

        # Create and add a product to the database
        product = Product(name="Fedora", description="A red hat", price=12.50, available=True, category=Category.CLOTHS)
        db.session.add(product)
        db.session.commit()

        # Use the find_by_name method to find the product
        found_product = Product.find_by_name("Fedora")

        # Assert that the product returned is the one we expect
        self.assertIsNotNone(found_product)
        self.assertEqual(found_product.name, "Fedora")
        self.assertEqual(found_product.description, "A red hat")
        self.assertEqual(found_product.price, 12.50)
        self.assertEqual(found_product.available, True)
        self.assertEqual(found_product.category, Category.CLOTHS)

        # Test for a non-existent product (should return None)
        non_existent_product = Product.find_by_name("NonExistentProduct")
        self.assertIsNone(non_existent_product)


#find by category
    def test_find_product_by_category(self):
        """It should find products by their category"""

        # Create and add products to the database
        product1 = Product(name="Fedora", description="A red hat", price=12.50, available=True, category=Category.CLOTHS)
        product2 = Product(name="Jeans", description="Blue denim jeans", price=30.00, available=True, category=Category.CLOTHS)
        product3 = Product(name="Shampoo", description="Hair care shampoo", price=5.00, available=True, category=Category.BEAUTY)

        db.session.add_all([product1, product2, product3])
        db.session.commit()

        # Use the find_by_category method to find products in the "Cloths" category
        cloths_products = Product.find_by_category(Category.CLOTHS)

        # Assert that products returned are in the "Cloths" category
        self.assertEqual(len(cloths_products), 2)
        self.assertTrue(all(product.category == Category.CLOTHS for product in cloths_products))
        self.assertIn(product1, cloths_products)
        self.assertIn(product2, cloths_products)

        # Assert that products in the "Beauty" category are not returned
        beauty_products = Product.find_by_category(Category.BEAUTY)
        self.assertEqual(len(beauty_products), 1)
        self.assertIn(product3, beauty_products)

        # Test for a non-existent category (should return an empty list)
        non_existent_category_products = Product.find_by_category("NonExistentCategory")
        self.assertEqual(len(non_existent_category_products), 0)

# find by availability              
    def test_find_product_by_availability(self):
        """It should find products by their availability (available or not)"""

        # Create and add products to the database with different availability
        product1 = Product(name="Fedora", description="A red hat", price=12.50, available=True, category=Category.CLOTHS)
        product2 = Product(name="Jeans", description="Blue denim jeans", price=30.00, available=False, category=Category.CLOTHS)
        product3 = Product(name="Shampoo", description="Hair care shampoo", price=5.00, available=True, category=Category.BEAUTY)

        db.session.add_all([product1, product2, product3])
        db.session.commit()

        # Use the find_by_availability method to find available products
        available_products = Product.find_by_availability(True)

        # Assert that only available products are returned
        self.assertEqual(len(available_products), 2)
        self.assertTrue(all(product.available is True for product in available_products))
        self.assertIn(product1, available_products)
        self.assertIn(product3, available_products)

        # Use the find_by_availability method to find unavailable products
        unavailable_products = Product.find_by_availability(False)

        # Assert that only unavailable products are returned
        self.assertEqual(len(unavailable_products), 1)
        self.assertTrue(all(product.available is False for product in unavailable_products))
        self.assertIn(product2, unavailable_products)

        # Test for products with availability status not specified (should return empty list or handle accordingly)
        no_availability_products = Product.find_by_availability(None)
        self.assertEqual(len(no_availability_products), 0)
