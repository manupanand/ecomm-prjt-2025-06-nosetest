Feature: The product store service back-end
    As a Product Store Owner
    I need a RESTful catalog service
    So that I can keep track of all my products

Background:
    Given the following products
        | name       | description     | price   | available | category   |
        | Hat        | A red fedora    | 59.95   | True      | CLOTHS     |
        | Shoes      | Blue shoes      | 120.50  | False     | CLOTHS     |
        | Big Mac    | 1/4 lb burger   | 5.99    | True      | FOOD       |
        | Sheets     | Full bed sheets | 87.00   | True      | HOUSEWARES |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Product Catalog Administration" in the title
    And I should not see "404 Not Found"

Scenario: Create a Product
    When I visit the "Home Page"
    And I set the "Name" to "Hammer"
    And I set the "Description" to "Claw hammer"
    And I select "True" in the "Available" dropdown
    And I select "Tools" in the "Category" dropdown
    And I set the "Price" to "34.95"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Description" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Hammer" in the "Name" field
    And I should see "Claw hammer" in the "Description" field
    And I should see "True" in the "Available" dropdown
    And I should see "Tools" in the "Category" dropdown
    And I should see "34.95" in the "Price" field

Feature: Update a Product
  As a user
  I want to update an existing product in the system
  So that I can correct or change its details

  Background:
    Given the database contains the following products:
      | id | name        | price | description         | stock |
      | 1  | Product One | 100   | First product       | 10    |
      | 2  | Product Two | 200   | Second product      | 20    |

  Scenario: Successfully updating a product with valid data
    Given a product with id "1" exists
    When I send a PUT request to "/products/1" with the following data:
      """
      {
        "name": "Updated Product One",
        "price": 150,
        "description": "Updated description for Product One",
        "stock": 15
      }
      """
    Then the response status code should be 200
    And the response body should contain:
      """
      {
        "id": 1,
        "name": "Updated Product One",
        "price": 150,
        "description": "Updated description for Product One",
        "stock": 15
      }
      """
    And the database should contain the updated product:
      | id | name                | price | description                    | stock |
      | 1  | Updated Product One | 150   | Updated description for Product One | 15    |

  Scenario: Attempting to update a product with invalid data
    Given a product with id "1" exists
    When I send a PUT request to "/products/1" with the following data:
      """
      {
        "name": "",
        "price": -50,
        "description": "Invalid product update",
        "stock": -10
      }
      """
    Then the response status code should be 400
    And the response body should contain an error message:
      """
      {
        "error": "Invalid input data",
        "details": {
          "name": "Name cannot be empty",
          "price": "Price must be greater than 0",
          "stock": "Stock must be non-negative"
        }
      }
      """

  Scenario: Attempting to update a non-existent product
    Given no product with id "999" exists
    When I send a PUT request to "/products/999" with the following data:
      """
      {
        "name": "Nonexistent Product",
        "price": 300,
        "description": "This product does not exist",
        "stock": 30
      }
      """
    Then the response status code should be 404
    And the response body should contain an error message:
      """
      {
        "error": "Product not found"
      }
      """

Feature: Read Products
  As a user
  I want to retrieve product details from the system
  So that I can view the product information

  Background:
    Given the database contains the following products:
      | id | name        | price | description         | stock |
      | 1  | Product One | 100   | First product       | 10    |
      | 2  | Product Two | 200   | Second product      | 20    |
      | 3  | Product Three | 300 | Third product       | 30    |

  Scenario: Successfully reading a product by ID
    Given a product with id "1" exists
    When I send a GET request to "/products/1"
    Then the response status code should be 200
    And the response body should contain:
      """
      {
        "id": 1,
        "name": "Product One",
        "price": 100,
        "description": "First product",
        "stock": 10
      }
      """

  Scenario: Attempting to read a non-existent product by ID
    Given no product with id "999" exists
    When I send a GET request to "/products/999"
    Then the response status code should be 404
    And the response body should contain an error message:
      """
      {
        "error": "Product not found"
      }
      """

  Scenario: Successfully reading all products
    When I send a GET request to "/products"
    Then the response status code should be 200
    And the response body should contain a list of products:
      """
      [
        {
          "id": 1,
          "name": "Product One",
          "price": 100,
          "description": "First product",
          "stock": 10
        },
        {
          "id": 2,
          "name": "Product Two",
          "price": 200,
          "description": "Second product",
          "stock": 20
        },
        {
          "id": 3,
          "name": "Product Three",
          "price": 300,
          "description": "Third product",
          "stock": 30
        }
      ]
      """

Feature: Delete Products
  As an admin
  I want to delete a product from the system
  So that I can manage the product inventory effectively

  Background:
    Given the database contains the following products:
      | id | name        | price | description         | stock |
      | 1  | Product One | 100   | First product       | 10    |
      | 2  | Product Two | 200   | Second product      | 20    |
      | 3  | Product Three | 300 | Third product       | 30    |

  Scenario: Successfully deleting a product
    Given a product with id "2" exists
    When I send a DELETE request to "/products/2"
    Then the response status code should be 200
    And the response body should contain a success message:
      """
      {
        "message": "Product deleted successfully"
      }
      """
    And the database should not contain a product with id "2"

  Scenario: Attempting to delete a non-existent product
    Given no product with id "999" exists
    When I send a DELETE request to "/products/999"
    Then the response status code should be 404
    And the response body should contain an error message:
      """
      {
        "error": "Product not found"
      }
      """

  Scenario: Attempting to delete a product without proper authorization
    Given a product with id "3" exists
    When I send a DELETE request to "/products/3" without valid credentials
    Then the response status code should be 403
    And the response body should contain an error message:
      """
      {
        "error": "Unauthorized access"
      }
      """
Feature: List All Products
  As a user or admin
  I want to retrieve a list of all products
  So that I can view the available products in the system

  Background:
    Given the database contains the following products:
      | id | name         | price | description        | stock |
      | 1  | Product One  | 100   | First product      | 10    |
      | 2  | Product Two  | 200   | Second product     | 20    |
      | 3  | Product Three| 300   | Third product      | 30    |

  Scenario: Successfully listing all products
    When I send a GET request to "/products"
    Then the response status code should be 200
    And the response body should contain:
      """
      [
        {
          "id": 1,
          "name": "Product One",
          "price": 100,
          "description": "First product",
          "stock": 10
        },
        {
          "id": 2,
          "name": "Product Two",
          "price": 200,
          "description": "Second product",
          "stock": 20
        },
        {
          "id": 3,
          "name": "Product Three",
          "price": 300,
          "description": "Third product",
          "stock": 30
        }
      ]
      """

  Scenario: Listing products when no products exist
    Given the database is empty
    When I send a GET request to "/products"
    Then the response status code should be 200
    And the response body should contain:
      """
      []
      """

  Scenario: Attempting to list products with invalid authorization
    When I send a GET request to "/products" without valid credentials
    Then the response status code should be 403
    And the response body should contain an error message:
      """
      {
        "error": "Unauthorized access"
      }
      """

Feature: Search Products by Category
  As a user or admin
  I want to search for products based on their category
  So that I can view only the relevant products in the system

  Background:
    Given the database contains the following products:
      | id | name         | category   | price | description        | stock |
      | 1  | Product One  | Electronics| 100   | First product      | 10    |
      | 2  | Product Two  | Clothing   | 200   | Second product     | 20    |
      | 3  | Product Three| Electronics| 300   | Third product      | 30    |
      | 4  | Product Four | Clothing   | 400   | Fourth product     | 40    |

  Scenario: Successfully searching products by category
    When I send a GET request to "/products?category=Electronics"
    Then the response status code should be 200
    And the response body should contain:
      """
      [
        {
          "id": 1,
          "name": "Product One",
          "category": "Electronics",
          "price": 100,
          "description": "First product",
          "stock": 10
        },
        {
          "id": 3,
          "name": "Product Three",
          "category": "Electronics",
          "price": 300,
          "description": "Third product",
          "stock": 30
        }
      ]
      """

  Scenario: Searching for products in a category with no products
    When I send a GET request to "/products?category=HomeAppliances"
    Then the response status code should be 200
    And the response body should contain:
      """
      []
      """

  Scenario: Attempting to search products without specifying a category
    When I send a GET request to "/products?category="
    Then the response status code should be 400
    And the response body should contain an error message:
      """
      {
        "error": "Category is required for searching products"
      }
      """

  Scenario: Searching for products with invalid authorization
    When I send a GET request to "/products?category=Clothing" without valid credentials
    Then the response status code should be 403
    And the response body should contain an error message:
      """
      {
        "error": "Unauthorized access"
      }
      """


Feature: Search Products by Availability
  As a user or admin
  I want to search for products based on their availability
  So that I can view only products that are in stock or out of stock

  Background:
    Given the database contains the following products:
      | id | name          | category      | price | description         | stock |
      | 1  | Product One   | Electronics   | 100   | First product       | 10    |
      | 2  | Product Two   | Clothing      | 200   | Second product      | 0     |
      | 3  | Product Three | Electronics   | 300   | Third product       | 5     |
      | 4  | Product Four  | Clothing      | 400   | Fourth product      | 0     |

  Scenario: Successfully searching products that are in stock
    When I send a GET request to "/products?availability=in_stock"
    Then the response status code should be 200
    And the response body should contain:
      """
      [
        {
          "id": 1,
          "name": "Product One",
          "category": "Electronics",
          "price": 100,
          "description": "First product",
          "stock": 10
        },
        {
          "id": 3,
          "name": "Product Three",
          "category": "Electronics",
          "price": 300,
          "description": "Third product",
          "stock": 5
        }
      ]
      """

  Scenario: Successfully searching products that are out of stock
    When I send a GET request to "/products?availability=out_of_stock"
    Then the response status code should be 200
    And the response body should contain:
      """
      [
        {
          "id": 2,
          "name": "Product Two",
          "category": "Clothing",
          "price": 200,
          "description": "Second product",
          "stock": 0
        },
        {
          "id": 4,
          "name": "Product Four",
          "category": "Clothing",
          "price": 400,
          "description": "Fourth product",
          "stock": 0
        }
      ]
      """

  Scenario: Searching for products without specifying availability
    When I send a GET request to "/products?availability="
    Then the response status code should be 400
    And the response body should contain an error message:
      """
      {
        "error": "Availability parameter is required for searching products"
      }
      """

  Scenario: Attempting to search products with invalid authorization
    When I send a GET request to "/products?availability=in_stock" without valid credentials
    Then the response status code should be 403
    And the response body should contain an error message:
      """
      {
        "error": "Unauthorized access"
      }
      """

Feature: Search Products by Name
  As a user or admin
  I want to search for products by their name
  So that I can quickly find a specific product

  Background:
    Given the database contains the following products:
      | id | name          | category      | price | description         | stock |
      | 1  | Product One   | Electronics   | 100   | First product       | 10    |
      | 2  | Product Two   | Clothing      | 200   | Second product      | 0     |
      | 3  | Product Three | Electronics   | 300   | Third product       | 5     |
      | 4  | Product Four  | Clothing      | 400   | Fourth product      | 0     |

  Scenario: Successfully searching products by exact name
    When I send a GET request to "/products?name=Product One"
    Then the response status code should be 200
    And the response body should contain:
      """
      [
        {
          "id": 1,
          "name": "Product One",
          "category": "Electronics",
          "price": 100,
          "description": "First product",
          "stock": 10
        }
      ]
      """

  Scenario: Successfully searching products by partial name match
    When I send a GET request to "/products?name=Product"
    Then the response status code should be 200
    And the response body should contain:
      """
      [
        {
          "id": 1,
          "name": "Product One",
          "category": "Electronics",
          "price": 100,
          "description": "First product",
          "stock": 10
        },
        {
          "id": 2,
          "name": "Product Two",
          "category": "Clothing",
          "price": 200,
          "description": "Second product",
          "stock": 0
        },
        {
          "id": 3,
          "name": "Product Three",
          "category": "Electronics",
          "price": 300,
          "description": "Third product",
          "stock": 5
        },
        {
          "id": 4,
          "name": "Product Four",
          "category": "Clothing",
          "price": 400,
          "description": "Fourth product",
          "stock": 0
        }
      ]
      """

  Scenario: No products found when searching by non-existent name
    When I send a GET request to "/products?name=NonExistentProduct"
    Then the response status code should be 200
    And the response body should contain:
      """
      []
      """

  Scenario: Searching for products by name with special characters
    When I send a GET request to "/products?name=Product One!"
    Then the response status code should be 200
    And the response body should contain:
      """
      [
        {
          "id": 1,
          "name": "Product One!",
          "category": "Electronics",
          "price": 100,
          "description": "First product with special character",
          "stock": 10
        }
      ]
      """

  Scenario: Attempting to search products without specifying a name
    When I send a GET request to "/products?name="
    Then the response status code should be 400
    And the response body should contain an error message:
      """
      {
        "error": "Product name parameter is required for searching"
      }
      """

  Scenario: Attempting to search products with invalid authorization
    When I send a GET request to "/products?name=Product One" without valid credentials
    Then the response status code should be 403
    And the response body should contain an error message:
      """
      {
        "error": "Unauthorized access"
      }
      """
