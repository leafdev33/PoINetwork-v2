import unittest
import threading
from poinetwork import Network
from poinode import Node
from interaction import Interaction
from Crypto.PublicKey import RSA

class TestNetwork(unittest.TestCase):

    def test_network(self):
        # Start the network on a separate thread
        network = Network("localhost", 5000)
        network_thread = threading.Thread(target=network.start)
        network_thread.daemon = True
        network_thread.start()

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

if __name__ == '__main__':
    unittest.main()