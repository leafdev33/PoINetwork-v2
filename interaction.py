import time
import json
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256

class Interaction:
    def __init__(self, data, public_key, recipient, points):
        self.timestamp = time.time()
        self.data = data
        self.public_key = RSA.importKey(public_key)
        self.recipient = RSA.importKey(recipient)
        self.signature = None
        self.points = points
    
    def __eq__(self, other):
        if isinstance(other, Interaction):
            return (self.timestamp == other.timestamp and
                    self.data == other.data and
                    self.public_key.export_key() == other.public_key.export_key() and
                    self.recipient.export_key() == other.recipient.export_key() and
                    self.signature == other.signature and
                    self.points == other.points)
        return False

    def sign(self, private_key):
        if not isinstance(private_key, RSA.RsaKey):
            private_key = RSA.importKey(private_key)
        hashed_data = SHA256.new(self.data.encode('utf-8'))
        signer = PKCS1_v1_5.new(private_key)
        self.signature = signer.sign(hashed_data)

    def verify_signature(self):
        if not self.signature or not self.public_key:
            return False

        hashed_data = SHA256.new(self.data.encode('utf-8'))
        verifier = PKCS1_v1_5.new(self.public_key)
        return verifier.verify(hashed_data, self.signature)

    def verify_interaction(self):
        return self.verify_signature()

    def serialize(self):
        interaction_data = {
            'timestamp': self.timestamp,
            'data': self.data,
            'public_key': self.public_key.export_key().decode('utf-8'),
            'recipient': self.recipient.export_key().decode('utf-8'),
            'signature': self.signature.hex(),
            'points': self.points
        }
        return json.dumps(interaction_data)

    @classmethod
    def deserialize(cls, json_data):
        interaction_data = json.loads(json_data)
        interaction = cls(
            interaction_data['data'],
            interaction_data['public_key'],
            interaction_data['recipient'],
            interaction_data['points']
        )
        interaction.timestamp = interaction_data['timestamp']
        interaction.signature = bytes.fromhex(interaction_data['signature'])
        return interaction
