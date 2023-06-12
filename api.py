# api.py

from flask import Flask, request, jsonify
from poinode import Node
from pointoken import Token
from interaction import Interaction
import threading
import time

app = Flask(__name__)

# Initialize a new node. You might want to load an existing blockchain or create a new one.
node = Node()

# This function simulates a node running in the background.
def node_simulation():
    while True:
        # Place any code here that should be executed regularly (e.g., mining, consensus)
        time.sleep(1)

# Run the node simulation in the background.
t = threading.Thread(target=node_simulation)
t.daemon = True
t.start()

# Endpoints

# Endpoint to create and broadcast an interaction
@app.route('/interactions', methods=['POST'])
def create_interaction():
    try:
        # Assume the request data contains the required fields for an interaction
        data = request.json
        interaction = node.create_interaction(
            data['data'],
            data['public_key'],
            data['recipient_public_key'],
            data['private_key'],
            data['points']
        )
        node.broadcast_interaction(interaction)

        return jsonify({"message": "Interaction created and broadcasted"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Endpoint to get the balance of a public key
@app.route('/balance/<public_key>', methods=['GET'])
def get_balance(public_key):
    balance = node.get_balance(public_key)
    return jsonify({"public_key": public_key, "balance": balance})

# Endpoint to get the full blockchain
@app.route('/blockchain', methods=['GET'])
def get_blockchain():
    blockchain = node.blockchain.serialize()
    return jsonify({"blockchain": blockchain})

# Main
if __name__ == '__main__':
    # Run Flask app on port 5000
    app.run(host='0.0.0.0', port=5000)
