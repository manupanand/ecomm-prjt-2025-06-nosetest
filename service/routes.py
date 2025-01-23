
"""
Product Store Service with UI
"""
from flask import jsonify, request, abort
from flask import url_for  # noqa: F401 pylint: disable=unused-import
from service.models import Product
from service.common import status  # HTTP Status Codes
from . import app


######################################################################
# H E A L T H   C H E C K
######################################################################
@app.route("/health")
def healthcheck():
    """Let them know our heart is still beating"""
    return jsonify(status=200, message="OK"), status.HTTP_200_OK


######################################################################
# H O M E   P A G E
######################################################################
@app.route("/")
def index():
    """Base URL for our service"""
    return app.send_static_file("index.html")


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################
def check_content_type(content_type):
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        app.logger.error("No Content-Type specified.")
        abort(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}",
        )

    if request.headers["Content-Type"] == content_type:
        return

    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {content_type}",
    )


######################################################################
# C R E A T E   A   N E W   P R O D U C T
######################################################################
@app.route("/products", methods=["POST"])
def create_products():
    """
    Creates a Product
    This endpoint will create a Product based the data in the body that is posted
    """
    app.logger.info("Request to Create a Product...")
    check_content_type("application/json")

    data = request.get_json()
    app.logger.info("Processing: %s", data)
    product = Product()
    product.deserialize(data)
    product.create()
    app.logger.info("Product with new id [%s] saved!", product.id)

    message = product.serialize()

    #
    # Uncomment this line of code once you implement READ A PRODUCT
    #
    # location_url = url_for("get_products", product_id=product.id, _external=True)
    location_url = "/"  # delete once READ is implemented
    return jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}


# List all products
@app.route("/products", methods=["GET"])
def list_products():
    products = Product.all()
    return jsonify([product.serialize() for product in products]), 200

# List products by name
@app.route("/products/name/<string:name>", methods=["GET"])
def list_products_by_name(name):
    products = Product.find_by_name(name)  # Retrieves products filtered by name
    if not products:
        abort(404, f"No products found with name '{name}'.")
    return jsonify([product.serialize() for product in products]), 200

# List products by category
@app.route("/products/category/<string:category>", methods=["GET"])
def list_products_by_category(category):
    products = Product.find_by_category(category)  # Retrieves products filtered by category
    if not products:
        abort(404, f"No products found in category '{category}'.")
    return jsonify([product.serialize() for product in products]), 200

# Get a single product by ID
@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = Product.find(product_id)
    if not product:
        abort(404, f"Product with ID {product_id} not found.")
    return jsonify(product.serialize()), 200

# List products by availability
@app.route("/products/availability/<bool:available>", methods=["GET"])
def list_products_by_availability(available):
    products = Product.find_by_availability(available)  # Retrieves products filtered by availability
    if not products:
        abort(404, f"No products found with availability status '{available}'.")
    return jsonify([product.serialize() for product in products]), 200

# Create a new product
@app.route("/products", methods=["POST"])
def create_product():
    data = request.get_json()
    product = Product()
    product.deserialize(data)
    product.create()
    return jsonify(product.serialize()), 201

# Update an existing product
@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    product = Product.find(product_id)
    if not product:
        abort(404, f"Product with ID {product_id} not found.")
    data = request.get_json()
    product.deserialize(data)
    product.update()
    return jsonify(product.serialize()), 200

# Delete a product
@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    product = Product.find(product_id)
    if not product:
        abort(404, f"Product with ID {product_id} not found.")
    product.delete()
    return "", 204

