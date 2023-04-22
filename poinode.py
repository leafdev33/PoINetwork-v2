from blockchain import Blockchain
from pointoken import Token
from interaction import Interaction
from consensus import PoIConsensus

class Node:
    def __init__(self):
        self.blockchain = Blockchain()
        self.token_balances = {}
        self.poi_consensus = PoIConsensus(self.blockchain)

    def create_interaction(self, sender, recipient, amount, private_key):
        if self.token_balances.get(sender) is None or self.token_balances[sender] < amount:
            return None

        interaction = Interaction(sender, recipient, amount)
        interaction.sign(private_key)
        return interaction

    def broadcast_interaction(self, interaction, network):
        if interaction.verify_signature() and interaction.sender != interaction.recipient:
            network.broadcast_interaction(self, interaction)

    def receive_interaction(self, interaction):
        if interaction.verify_signature():
            self.poi_consensus.add_interaction(interaction)

    def validate_and_add_block(self, block):
        if self.poi_consensus.validate_block(block):
            self.blockchain.add_block(block.interactions)
            self.update_balances(block.interactions)

    def update_balances(self, interactions):
        for interaction in interactions:
            if isinstance(interaction, Token):
                if self.token_balances.get(interaction.receiver) is None:
                    self.token_balances[interaction.receiver] = 0
                self.token_balances[interaction.receiver] += interaction.amount
            else:
                if self.token_balances.get(interaction.sender) is None:
                    self.token_balances[interaction.sender] = 0
                if self.token_balances.get(interaction.receiver) is None:
                    self.token_balances[interaction.receiver] = 0
                self.token_balances[interaction.sender] -= interaction.amount
                self.token_balances[interaction.receiver] += interaction.amount


    def get_balance(self, public_key):
        return self.token_balances.get(public_key, 0)
