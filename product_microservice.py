from flask import Flask, request, jsonify

app = Flask(__name__)
products = {}  # In-memory "database"
product_id_counter = 1

# CREATE
@app.route('/products', methods=['POST'])
def create_product():
    global product_id_counter
    data = request.json
    product_id = str(product_id_counter)
    products[product_id] = {'id': product_id, 'name': data['name'], 'price': data['price']}
    product_id_counter += 1
    return jsonify(products[product_id]), 201

# READ (all)
@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(list(products.values()))

# READ (one)
@app.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    product = products.get(product_id)
    if product:
        return jsonify(product)
    return jsonify({'error': 'Product not found'}), 404

# UPDATE
@app.route('/products/<product_id>', methods=['PUT'])
def update_product(product_id):
    if product_id not in products:
        return jsonify({'error': 'Product not found'}), 404
    data = request.json
    products[product_id].update({'name': data['name'], 'price': data['price']})
    return jsonify(products[product_id])

# DELETE
@app.route('/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    if product_id in products:
        deleted = products.pop(product_id)
        return jsonify({'message': 'Deleted', 'product': deleted})
    return jsonify({'error': 'Product not found'}), 404

if __name__ == '__main__':
    app.run(port=5000)
