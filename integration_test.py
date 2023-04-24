import unittest
import threading
from blockchain import Blockchain
from interaction import Interaction
from consensus import PoIConsensus
from pointoken import Token, SignedTransaction
from poinode import Node
from poinetwork import Network
import time
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
        interaction1 = Interaction('like - post1', public_key1, public_key2, 10)
        interaction2 = Interaction('share - post2', public_key1, public_key2, 15)  # Added recipient argument
        interaction3 = Interaction('like - post1', public_key2, public_key1, 10)  # Updated the recipient to public_key1

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
        node = Node()

        key = RSA.generate(2048)
        pubkey1 = key.publickey().export_key()
        private_key1 = key.export_key()

        key = RSA.generate(2048)
        pubkey2 = key.publickey().export_key()

        # Add initial tokens to pubkey1
        node.token.add_tokens(pubkey1, 1000)

        event = "Test event: token transfer"
        interaction1 = node.create_interaction(event, pubkey1, pubkey2, private_key1, 10)
        interaction2 = node.create_interaction(event, pubkey1, pubkey2, private_key1, 200)

        # Test interaction verification
        self.assertTrue(interaction1.verify_signature())

        # Test updating balances with interactions
        node.update_balances([interaction1, interaction2])

        # Check if the balances have been updated correctly
        self.assertEqual(node.get_balance(pubkey1), 790)  # 1000 initial - 210 points
        self.assertEqual(node.get_balance(pubkey2), 210)  # pubkey2 receives 210 points (10 + 200) from interactions

class TestNetworkIntegration(unittest.TestCase):

    def setUp(self):
        self.network = Network("localhost", 5000)
        network_thread = threading.Thread(target=self.network.start)
        network_thread.daemon = True
        network_thread.start()
        time.sleep(1)  # Add a short delay to allow the network to start

        self.node1 = Node()
        self.node2 = Node()
        self.node1.connect("localhost", 5000)
        self.node2.connect("localhost", 5000)
        time.sleep(1)  # Add a short delay to allow the nodes to connect

    def test_network_integration(self):
        # Generate a key pair for the node
        key = RSA.generate(2048)
        public_key = key.publickey().exportKey()
        private_key = key.export_key()

        # Generate a key pair for the recipient
        recipient_key = RSA.generate(2048)
        recipient_public_key = recipient_key.publickey().exportKey()

        # Create two nodes and connect to the network
        node1 = Node()
        node2 = Node()
        node1.connect("localhost", 5000)
        node2.connect("localhost", 5000)

        # Create an interaction and sign it
        interaction = node1.create_interaction("Test interaction", public_key, recipient_public_key, private_key, 10)

        # Send the interaction from node1
        node1.broadcast_interaction(interaction)

        # Verify that node2 received the interaction
        received_interaction = node2.receive_interaction()
        self.assertEqual(interaction, received_interaction)

    def tearDown(self):
        self.node1.connection.close()
        self.node2.connection.close()
        time.sleep(1)  # Allow time for sockets to close
        self.network.server.close()
        
if __name__ == '__main__':
    unittest.main()