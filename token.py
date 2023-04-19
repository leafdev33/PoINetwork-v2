from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256

class SignedTransaction:
    def __init__(self, sender, recipient, amount, signature=None):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = signature

    def sign(self, private_key):
        message = f"{self.sender}:{self.recipient}:{self.amount}"
        hashed_message = SHA256.new(message.encode('utf-8'))
        signer = PKCS1_v1_5.new(private_key)
        self.signature = signer.sign(hashed_message)

    def verify(self, public_key):
        message = f"{self.sender}:{self.recipient}:{self.amount}"
        hashed_message = SHA256.new(message.encode('utf-8'))
        verifier = PKCS1_v1_5.new(public_key)
        return verifier.verify(hashed_message, self.signature)

class Token:
    def __init__(self):
        self.balances = {}

    def create_tokens(self, address, amount):
        """
        Creates tokens and assigns them to the specified address.
        """
        if address not in self.balances:
            self.balances[address] = 0
        self.balances[address] += amount

    def transfer_tokens(self, signed_transaction):
        """
        Transfers tokens based on the information in a signed transaction.
        """
        sender = signed_transaction.sender
        recipient = signed_transaction.recipient
        amount = signed_transaction.amount

        if sender not in self.balances:
            raise ValueError("Sender address not found.")
        if recipient not in self.balances:
            self.balances[recipient] = 0

        if self.balances[sender] < amount:
            raise ValueError("Insufficient balance.")

        if not signed_transaction.verify(sender):
            raise ValueError("Invalid transaction signature.")

        self.balances[sender] -= amount
        self.balances[recipient] += amount


    def get_balance(self, address):
        """
        Returns the token balance for the specified address.
        """
        if address not in self.balances:
            return 0
        return self.balances[address]
