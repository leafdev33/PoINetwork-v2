import unittest
import threading
from network import Network
from poinode import Node

class TestNetwork(unittest.TestCase):

    def test_network(self):
        # Start the network on a separate thread
        network = Network("localhost", 5000)
        network_thread = threading.Thread(target=network.start)
        network_thread.daemon = True
        network_thread.start()

        # Create two nodes and connect to the network
        node1 = Node()
        node2 = Node()
        node1.connect("localhost", 5000)
        node2.connect("localhost", 5000)

        # Send an interaction from node1 to node2
        interaction = node1.create_interaction("Test interaction", node1.public_key, node1.private_key, 10)
        node1.send_interaction(interaction)

        # Verify that node2 received the interaction
        received_interaction = node2.receive_interaction()
        self.assertEqual(interaction, received_interaction)

if __name__ == '__main__':
    unittest.main()
