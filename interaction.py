import time
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256

class Interaction:
    def __init__(self, data, public_key):
        self.timestamp = time.time()
        self.data = data
        self.public_key = RSA.importKey(public_key)
        self.signature = None

    def sign(self, private_key):
        private_key = RSA.importKey(private_key)
        hashed_data = SHA256.new(self.data.encode('utf-8'))
        signer = PKCS1_v1_5.new(private_key)
        self.signature = signer.sign(hashed_data)

    def verify(self):
        if self.signature is None:
            return False

        hashed_data = SHA256.new(self.data.encode('utf-8'))
        verifier = PKCS1_v1_5.new(self.public_key)
        return verifier.verify(hashed_data, self.signature)

# Example usage:
# Generate a public/private key pair
key = RSA.generate(2048)
public_key = key.publickey().exportKey()
private_key = key.exportKey()

# Create an interaction
interaction = Interaction("Sample interaction data", public_key)

# Sign the interaction
interaction.sign(private_key)

# Verify the interaction
is_valid = interaction.verify()
print("Is the interaction valid?", is_valid)
