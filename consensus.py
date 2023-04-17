import random
from blockchain import Blockchain
from interaction import Interaction
from Crypto.PublicKey import RSA

class PoIConsensus:
    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.interaction_pool = []

    def add_interaction(self, interaction):
        if interaction.verify_signature():
            self.interaction_pool.append(interaction)
            return True
        return False

    def select_proposer(self, nodes):
        eligible_nodes = [node for node in nodes if node.is_eligible()]
        if not eligible_nodes:
            return None
        return random.choice(eligible_nodes)

    def validate_block(self, block, nodes):
        for interaction in block.interactions:
            if not interaction.verify_interaction():
                return False

        consensus_threshold = int(len(nodes) * 0.51) + 1
        valid_votes = 0

        for node in nodes:
            if node.validate_block(block):
                valid_votes += 1

            if valid_votes >= consensus_threshold:
                return True

        return False

    def update_interaction_pool(self, block):
        self.interaction_pool = [interaction for interaction in self.interaction_pool if interaction not in block.interactions]
