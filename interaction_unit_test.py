import unittest
from Crypto.PublicKey import RSA
from interaction import Interaction

class TestInteraction(unittest.TestCase):

    def test_create_sign_and_verify_interaction(self):
        # Generate a public/private key pair
        key = RSA.generate(2048)
        public_key = key.publickey().exportKey()
        private_key = key.exportKey()

        # Create an interaction
        interaction = Interaction("Sample interaction data", public_key)

        # Sign the interaction
        interaction.sign(private_key)

        # Verify the interaction
        self.assertTrue(interaction.verify_signature())

    def test_verify_invalid_signature(self):
        # Generate a public/private key pair
        key1 = RSA.generate(2048)
        public_key1 = key1.publickey().exportKey()
        private_key1 = key1.exportKey()

        # Generate another public/private key pair
        key2 = RSA.generate(2048)
        public_key2 = key2.publickey().exportKey()
        private_key2 = key2.exportKey()

        # Create an interaction using public_key1
        interaction = Interaction("Sample interaction data", public_key1)

        # Sign the interaction with private_key2
        interaction.sign(private_key2)

        # Verify the interaction using public_key1 (expecting False since the wrong key was used to sign)
        self.assertFalse(interaction.verify_signature())

if __name__ == '__main__':
    unittest.main()
