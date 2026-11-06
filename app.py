import hashlib
import json
import time
from flask import Flask, request, jsonify

app = Flask(__name__)


class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.create_block(proof=100, previous_hash="1")

    def create_block(self, proof, previous_hash):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": time.time(),
            "transactions": self.pending_transactions,
            "proof": proof,
            "previous_hash": previous_hash
        }
        self.pending_transactions = []
        self.chain.append(block)
        return block

    def add_transaction(self, sender, receiver, amount):
        self.pending_transactions.append({
            "sender": sender,
            "receiver": receiver,
            "amount": amount
        })
        return len(self.chain) + 1

    @staticmethod
    def hash(block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def proof_of_work(self, previous_proof):
        new_proof = 1
        while True:
            value = str(new_proof ** 2 - previous_proof ** 2).encode()
            result = hashlib.sha256(value).hexdigest()
            if result[:4] == "0000":
                return new_proof
            new_proof += 1

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current["previous_hash"] != self.hash(previous):
                return False

            proof_value = current["proof"] ** 2 - previous["proof"] ** 2
            result = hashlib.sha256(str(proof_value).encode()).hexdigest()
            if result[:4] != "0000":
                return False

        return True


blockchain = Blockchain()


@app.route("/", methods=["GET"])
def home():
    return """
    <h1>Mini Blockchain Project</h1>
    <h2>Blockchain is running!</h2>
    <p>Available endpoints:</p>
    <ul>
      <li>GET /chain</li>
      <li>POST /transactions/new</li>
      <li>POST /mine</li>
      <li>GET /valid</li>
    </ul>
    """


@app.route("/chain", methods=["GET"])
def get_chain():
    return jsonify({
        "chain": blockchain.chain,
        "length": len(blockchain.chain)
    }), 200


@app.route("/transactions/new", methods=["POST"])
def new_transaction():
    values = request.get_json(silent=True)

    if not isinstance(values, dict):
        return jsonify({"error": "JSON body required"}), 400

    required = ["sender", "receiver", "amount"]
    if not all(key in values for key in required):
        return jsonify({"error": "Missing transaction fields"}), 400

    if not isinstance(values["sender"], str) or not values["sender"].strip():
        return jsonify({"error": "Invalid sender"}), 400

    if not isinstance(values["receiver"], str) or not values["receiver"].strip():
        return jsonify({"error": "Invalid receiver"}), 400

    amount = values["amount"]
    if isinstance(amount, bool) or not isinstance(amount, (int, float)) or amount <= 0:
        return jsonify({"error": "Amount must be positive"}), 400

    index = blockchain.add_transaction(
        values["sender"].strip(),
        values["receiver"].strip(),
        amount
    )
    return jsonify({"message": f"Transaction added for block {index}"}), 201


@app.route("/mine", methods=["POST"])
def mine():
    previous_block = blockchain.chain[-1]
    proof = blockchain.proof_of_work(previous_block["proof"])
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)

    return jsonify({
        "message": "New block successfully mined!",
        "index": block["index"],
        "transactions": block["transactions"],
        "proof": block["proof"],
        "previous_hash": block["previous_hash"]
    }), 200


@app.route("/valid", methods=["GET"])
def valid():
    is_valid = blockchain.is_chain_valid()
    return jsonify({
        "valid": is_valid,
        "message": "Blockchain is valid" if is_valid
                   else "Blockchain has been corrupted"
    }), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
