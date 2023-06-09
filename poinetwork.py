import socket
import threading
from queue import Queue
from poinode import Node

class Network:
    def __init__(self, host, port, max_connections=5):
        self.host = host
        self.port = port
        self.max_connections = max_connections
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.nodes = set()
        self.interaction_queue = Queue()

    def start(self):
        self.server.bind((self.host, self.port))
        self.server.listen(self.max_connections)
        print(f"Network listening on {self.host}:{self.port}")

        while True:
            conn, addr = self.server.accept()
            node = Node(connection=conn)
            self.nodes.add(node)
            threading.Thread(target=self.handle_node, args=(node,)).start()

    def handle_node(self, node):
        while True:
            try:
                interaction = node.receive_interaction()
                if interaction:
                    self.interaction_queue.put(interaction)
                    self.broadcast_interaction(interaction, sender_node=node)
            except Exception as e:
                print(f"Error handling node: {e}")
                self.nodes.remove(node)
                break

    def broadcast_interaction(self, interaction, sender_node=None):
        for node in self.nodes.copy():
            if node != sender_node:
                try:
                    node.broadcast_interaction(interaction)
                except Exception as e:
                    print(f"Error broadcasting interaction: {e}")
                    self.nodes.remove(node)