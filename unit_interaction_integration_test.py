import unittest
from interaction import Interaction
from block import Block
from blockchain import Blockchain
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256

class TestBlockchain(unittest.TestCase):
    def test_blockchain(self):
        # Generate a key pair
        key = RSA.generate(2048)
        public_key = key.publickey().export_key()

        # Create interactions with the public_key
        interaction1 = Interaction("data1", public_key)
        interaction2 = Interaction("data2", public_key)
        interaction3 = Interaction("data3", public_key)

        # Sign the interactions
        def sign_interaction(interaction, private_key):
            hashed_data = SHA256.new(interaction.data.encode('utf-8'))
            signer = PKCS1_v1_5.new(private_key)
            signature = signer.sign(hashed_data)
            interaction.signature = signature

        sign_interaction(interaction1, key)
        sign_interaction(interaction2, key)
        sign_interaction(interaction3, key)

        # Create a blockchain
        blockchain = Blockchain()

        # Add a block with interactions to the blockchain
        blockchain.add_block([interaction1, interaction2])

        # Add another block with an interaction to the blockchain
        blockchain.add_block([interaction3])

        # Test if the blockchain contains the correct number of blocks
        self.assertEqual(len(blockchain.chain), 3)

        # Test if the interactions were added to the blocks
        self.assertEqual(blockchain.chain[1].interactions, [interaction1, interaction2])
        self.assertEqual(blockchain.chain[2].interactions, [interaction3])

        # Test if the block hash is correctly calculated
        expected_block1_hash = blockchain.chain[1].calculate_hash()
        self.assertEqual(blockchain.chain[1].hash, expected_block1_hash)

        # Test if the block index and previous hash are correct
        self.assertEqual(blockchain.chain[1].index, 1)
        self.assertEqual(blockchain.chain[1].previous_hash, blockchain.chain[0].hash)

        # Test if the genesis block has correct values
        self.assertEqual(blockchain.chain[0].index, 0)
        self.assertEqual(blockchain.chain[0].previous_hash, "0")
        self.assertEqual(blockchain.chain[0].interactions, [])

if __name__ == "__main__":
    unittest.main()
