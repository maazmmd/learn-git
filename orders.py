from flask import Flask, request, jsonify

app = Flask(__name__)
orders = {}
order_id_counter = 1

@app.route('/orders', methods=['POST'])
def create_order():
    global order_id_counter
    data = request.json
    order_id = str(order_id_counter)
    orders[order_id] = {
        'id': order_id,
        'item': data['item'],
        'quantity': data['quantity'],
        'amount': data['amount'],
        'status': 'pending'  # e.g., pending, confirmed, shipped
    }
    order_id_counter += 1
    return jsonify(orders[order_id]), 201

@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify(list(orders.values()))

@app.route('/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    order = orders.get(order_id)
    if order:
        return jsonify(order)
    return jsonify({'error': 'Order not found'}), 404

@app.route('/orders/<order_id>', methods=['PUT'])
def update_order(order_id):
    if order_id not in orders:
        return jsonify({'error': 'Order not found'}), 404
    data = request.json
    orders[order_id].update({
        'item': data['item'],
        'quantity': data['quantity'],
        'amount': data['amount'],
        'status': data['status']
    })
    return jsonify(orders[order_id])

@app.route('/orders/<order_id>', methods=['DELETE'])
def delete_order(order_id):
    if order_id in orders:
        deleted = orders.pop(order_id)
        return jsonify({'message': 'Deleted', 'order': deleted})
    return jsonify({'error': 'Order not found'}), 404

if __name__ == '__main__':
    app.run(port=5001)
