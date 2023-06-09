import unittest
from Crypto.PublicKey import RSA
from pointoken import Token, SignedTransaction

class TestToken(unittest.TestCase):
    def test_token_and_signed_transaction(self):
        # Generate a key pair for two users
        key1 = RSA.generate(2048)
        public_key1 = key1.publickey().export_key()
        key2 = RSA.generate(2048)
        public_key2 = key2.publickey().export_key()

        # Initialize Token object
        token = Token()

        # Test initial balances
        token.add_tokens(public_key1, 100)
        self.assertEqual(token.balances[public_key1], 100)

        # Create a signed transaction
        transaction = SignedTransaction(public_key1, public_key2, 50)
        transaction.sign(key1.export_key())

        # Test transaction signing and verification
        self.assertTrue(transaction.verify(public_key1))
        self.assertFalse(transaction.verify(public_key2))

        # Test token transfer
        result = token.transfer_tokens(public_key1, public_key2, 50, transaction.signature)
        self.assertTrue(result)
        self.assertEqual(token.balances[public_key1], 50)
        self.assertEqual(token.balances[public_key2], 50)

        # Test invalid signature
        transaction.signature = b"fake_signature"
        result = token.transfer_tokens(public_key1, public_key2, 50, transaction.signature)
        self.assertFalse(result)

        # Test insufficient balance
        transaction = SignedTransaction(public_key1, public_key2, 200)
        transaction.sign(key1.export_key())
        result = token.transfer_tokens(public_key1, public_key2, 200, transaction.signature)
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()
