import unittest
from blockchain import Blockchain
from interaction import Interaction
from consensus import PoIConsensus
from pointoken import Token, SignedTransaction
from Crypto.PublicKey import RSA

class MockNode:
    def __init__(self):
        self.blockchain = Blockchain()
        self.poi_consensus = PoIConsensus(self.blockchain)
        self.token = Token()

class TestBlockchain(unittest.TestCase):
    def test_blockchain(self):
        # Create a mock node
        node = MockNode()

        # Generate a key pair for two users
        key1 = RSA.generate(2048)
        public_key1 = key1.publickey().export_key()
        key2 = RSA.generate(2048)
        public_key2 = key2.publickey().export_key()

        # Add initial tokens to a user
        node.token.add_tokens(public_key1, 100)

        # Create sample interactions
        interaction1 = Interaction('like - post1',public_key1)
        interaction2 = Interaction('share - post2', public_key1)
        interaction3 = Interaction('like - post1', public_key2)

        # Sign the interactions
        interaction1.sign(key1.exportKey())
        interaction2.sign(key1.exportKey())
        interaction3.sign(key2.exportKey())

        # Add interactions to the PoIConsensus
        node.poi_consensus.add_interaction(interaction1)
        node.poi_consensus.add_interaction(interaction2)
        node.poi_consensus.add_interaction(interaction3)

        self.assertEqual(len(node.poi_consensus.interaction_pool), 3)

        # Validate block with consensus nodes
        node.poi_consensus.validate_interactions()
        self.assertEqual(len(node.poi_consensus.interaction_pool), 0)

        # Add the confirmed interactions to the blockchain
        node.blockchain.add_block(node.poi_consensus.confirmed_interactions)
        self.assertEqual(len(node.blockchain.chain), 2)
        self.assertEqual(node.blockchain.chain[1].interactions, [interaction1, interaction2, interaction3])

        # Create and sign a transaction
        transaction = SignedTransaction(public_key1, public_key2, 50)
        transaction.sign(key1.export_key())

        # Test token transfer
        result = node.token.transfer_tokens(public_key1, public_key2, 50, transaction.signature)
        self.assertTrue(result)
        self.assertEqual(node.token.balances[public_key1], 50)
        self.assertEqual(node.token.balances[public_key2], 50)

        # Test invalid signature
        transaction.signature = b"fake_signature"
        result = node.token.transfer_tokens(public_key1, public_key2, 50, transaction.signature)
        self.assertFalse(result)

        # Test insufficient balance
        transaction = SignedTransaction(public_key1, public_key2, 200)
        transaction.sign(key1.export_key())
        result = node.token.transfer_tokens(public_key1, public_key2, 200, transaction.signature)
        self.assertFalse(result)

class TestNode(unittest.TestCase):
    def test_node(self):
        # Initialize a node and generate key pairs
        node1 = Node()
        key1 = RSA.generate(2048)
        pubkey1 = key1.publickey().export_key()
        private_key1 = key1.export_key()

        # Test token creation
        token = Token(1000, pubkey1)
        node1.update_balances([token])

        # Check if the token balance was updated correctly
        self.assertEqual(node1.get_balance(pubkey1), 1000)

        # Create another node and key pair
        node2 = Node()
        key2 = RSA.generate(2048)
        pubkey2 = key2.publickey().export_key()

        # Test creating and signing interactions
        interaction = node1.create_interaction(pubkey1, pubkey2, 200, private_key1)
        self.assertIsNotNone(interaction)

        # Test interaction verification
        self.assertTrue(interaction.verify_signature())

        # Test updating balances with interactions
        node1.update_balances([interaction])
        node2.update_balances([interaction])

        # Check if the balances have been updated correctly
        self.assertEqual(node1.get_balance(pubkey1), 800)
        self.assertEqual(node2.get_balance(pubkey2), 200)

        # ... additional tests for broadcasting and receiving interactions, adding blocks, etc. ...

if __name__ == '__main__':
    unittest.main()