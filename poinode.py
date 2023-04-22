from blockchain import Blockchain
from pointoken import Token
from interaction import Interaction
from consensus import PoIConsensus

class Node:
    def __init__(self):
        self.blockchain = Blockchain()
        self.poi_consensus = PoIConsensus(self.blockchain)
        self.token_balances = Token()

    def create_interaction(self, event, sender, private_key):
        interaction = Interaction(event, sender)
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
            # Add newly minted tokens as interactions to the block
            tokens = self.poi_consensus.mint_tokens(block)
            self.blockchain.add_block(block.interactions + tokens)
            self.update_balances(block.interactions + tokens)

    def update_balances(self, interactions):
        for interaction in interactions:
            if isinstance(interaction, Interaction):
                if self.token_balances.get(interaction.sender) is None:
                    self.token_balances[interaction.sender] = interaction.points
                else:
                    self.token_balances[interaction.sender] += interaction.points
            elif isinstance(interaction, Token):
                if self.token_balances.get(interaction.owner) is None:
                    self.token_balances[interaction.owner] = interaction.amount
                else:
                    self.token_balances[interaction.owner] += interaction.amount

                # Deduct the balance of the sender
                if self.token_balances.get(interaction.sender) is not None:
                    self.token_balances[interaction.sender] -= interaction.amount

    def get_balance(self, public_key):
        return self.token_balances.get(public_key, 0)