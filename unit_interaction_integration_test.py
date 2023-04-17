import unittest
from interaction import Interaction
from block import Block
from blockchain import Blockchain
from consensus import PoIConsensus
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256

class MockNode:
    def __init__(self):
        self.eligible = True

    def is_eligible(self):
        return self.eligible

    def validate_block(self, block):
        return True

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

        # Create a blockchain and PoIConsensus instance
        blockchain = Blockchain()
        poi_consensus = PoIConsensus(blockchain)

        # Add interactions to the interaction pool
        poi_consensus.add_interaction(interaction1)
        poi_consensus.add_interaction(interaction2)
        poi_consensus.add_interaction(interaction3)

        # Create a list of mock nodes
        nodes = [MockNode() for _ in range(5)]

        # Create a block with interactions
        new_block = Block(len(blockchain.chain), blockchain.get_latest_block().hash, [interaction1, interaction2])

        # Validate the block using the consensus rules
        is_valid = poi_consensus.validate_block(new_block, nodes)

        # If the block is valid, update the blockchain and interaction pool
        if is_valid:
            new_block.hash = new_block.calculate_hash()
            blockchain.chain.append(new_block)
            poi_consensus.update_interaction_pool(new_block)

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

            # Test if the interaction pool is updated correctly
            self.assertEqual(len(poi_consensus.interaction_pool), 1)
            self.assertEqual(poi_consensus.interaction_pool[0], interaction3)


if __name__ == "__main__":
    unittest.main()
