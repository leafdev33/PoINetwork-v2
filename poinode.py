import socket
import json
from blockchain import Blockchain
from pointoken import Token
from interaction import Interaction
from consensus import PoIConsensus

class Node:
    def __init__(self, connection=None):
        self.blockchain = Blockchain()
        self.poi_consensus = PoIConsensus(self.blockchain)
        self.token = Token()
        self.connection = connection

    def connect(self, host, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((host, port))

    def create_interaction(self, data, public_key, recipient_public_key, private_key, points):
        interaction = Interaction(data, public_key, recipient_public_key, points)
        interaction.sign(private_key)
        return interaction
    
    def broadcast_interaction(self, interaction):
        if interaction.verify_signature() and interaction.public_key != interaction.recipient:
            serialized_interaction = interaction.serialize()
            self.connection.send(serialized_interaction.encode())
    
    def receive_interaction(self):
        data = self.connection.recv(4096).decode()
        interaction = Interaction.deserialize(data)
        if interaction.verify_signature():
            self.poi_consensus.add_interaction(interaction)
        return interaction

    def validate_and_add_block(self, block):
        if self.poi_consensus.validate_block(block):
            # Add newly minted tokens as interactions to the block
            tokens = self.poi_consensus.mint_tokens(block)
            self.blockchain.add_block(block.interactions + tokens)
            self.update_balances(block.interactions + tokens)

    def update_balances(self, interactions):
        for interaction in interactions:
            if isinstance(interaction, Interaction):
                public_key_pem = interaction.public_key.export_key()
                if self.token.balances.get(public_key_pem) is None:
                    self.token.balances[public_key_pem] = interaction.points
                else:
                    self.token.balances[public_key_pem] += interaction.points
            elif isinstance(interaction, Token):
                if self.token.balances.get(interaction.owner) is None:
                    self.token.balances[interaction.owner] = interaction.amount
                else:
                    self.token.balances[interaction.owner] += interaction.amount

                # Deduct the balance of the sender
                if self.token.balances.get(interaction.sender) is not None:
                    self.token.balances[interaction.sender] -= interaction.amount

    def get_balance(self, public_key_pem):
        return self.token.balances.get(public_key_pem, 0)