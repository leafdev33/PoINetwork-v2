from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256

class Token:
    def __init__(self):
        self.balances = {}

    def add_tokens(self, public_key, amount):
        if public_key in self.balances:
            self.balances[public_key] += amount
        else:
            self.balances[public_key] = amount

    def transfer_tokens(self, sender_public_key, recipient_public_key, amount, signature):
        if self.verify_transaction(sender_public_key, recipient_public_key, amount, signature):
            self.balances[sender_public_key] -= amount
            self.add_tokens(recipient_public_key, amount)
            return True
        return False

    def verify_transaction(self, sender_public_key, recipient_public_key, amount, signature):
        signer_public_key = RSA.import_key(sender_public_key)
        hashed_message = SHA256.new(f"{sender_public_key}{recipient_public_key}{amount}".encode("utf-8"))
        verifier = PKCS1_v1_5.new(signer_public_key)
        return verifier.verify(hashed_message, signature)

class SignedTransaction:
    def __init__(self, sender_public_key, recipient_public_key, amount):
        self.sender_public_key = sender_public_key
        self.recipient_public_key = recipient_public_key
        self.amount = amount
        self.signature = None

    def sign(self, private_key):
        signer_private_key = RSA.import_key(private_key)
        hashed_message = SHA256.new(f"{self.sender_public_key}{self.recipient_public_key}{self.amount}".encode("utf-8"))
        signer = PKCS1_v1_5.new(signer_private_key)
        self.signature = signer.sign(hashed_message)

    def verify(self, public_key):
        signer_public_key = RSA.import_key(public_key)
        hashed_message = SHA256.new(f"{self.sender_public_key}{self.recipient_public_key}{self.amount}".encode("utf-8"))
        verifier = PKCS1_v1_5.new(signer_public_key)
        return verifier.verify(hashed_message, self.signature)