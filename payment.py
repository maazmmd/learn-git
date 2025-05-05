from flask import Flask, request, jsonify

app = Flask(__name__)
payments = {}  # In-memory "database"
payment_id_counter = 1

# CREATE
@app.route('/payments', methods=['POST'])
def create_payment():
    global payment_id_counter
    data = request.json
    payment_id = str(payment_id_counter)
    payments[payment_id] = {
        'id': payment_id,
        'payer': data['payer'],
        'amount': data['amount'],
        'method': data['method']  # e.g., 'credit_card', 'paypal'
    }
    payment_id_counter += 1
    return jsonify(payments[payment_id]), 201

# READ (all)
@app.route('/payments', methods=['GET'])
def get_payments():
    return jsonify(list(payments.values()))

# READ (one)
@app.route('/payments/<payment_id>', methods=['GET'])
def get_payment(payment_id):
    payment = payments.get(payment_id)
    if payment:
        return jsonify(payment)
    return jsonify({'error': 'Payment not found'}), 404

# UPDATE
@app.route('/payments/<payment_id>', methods=['PUT'])
def update_payment(payment_id):
    if payment_id not in payments:
        return jsonify({'error': 'Payment not found'}), 404
    data = request.json
    payments[payment_id].update({
        'payer': data['payer'],
        'amount': data['amount'],
        'method': data['method']
    })
    return jsonify(payments[payment_id])

# DELETE
@app.route('/payments/<payment_id>', methods=['DELETE'])
def delete_payment(payment_id):
    if payment_id in payments:
        deleted = payments.pop(payment_id)
        return jsonify({'message': 'Deleted', 'payment': deleted})
    return jsonify({'error': 'Payment not found'}), 404

if __name__ == '__main__':
    app.run(port=5000)