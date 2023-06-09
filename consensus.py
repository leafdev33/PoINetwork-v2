import random
from blockchain import Blockchain
from interaction import Interaction
from Crypto.PublicKey import RSA

class PoIConsensus:
    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.interaction_pool = []
        self.confirmed_interactions = []
        
    def add_block(self, interactions):
        new_block = Block(len(self.blockchain.chain), self.blockchain.get_latest_block().hash, interactions)
        self.blockchain.add_block(interactions)
        self.update_interaction_pool(new_block)
    
    def add_interaction(self, interaction):
        if interaction.verify_signature():
            self.interaction_pool.append(interaction)
            return True
        return False
    
    def validate_interactions(self):
    # Implement your consensus algorithm here.
    # For simplicity, let's consider all interactions in the pool as valid.
        self.confirmed_interactions = self.interaction_pool
        self.interaction_pool = []

    def select_proposer(self, nodes):
        eligible_nodes = [node for node in nodes if node.is_eligible()]
        if not eligible_nodes:
            return None
        return random.choice(eligible_nodes)
    
    def mint_tokens(self, block):
        tokens = []
        for pubkey, points in block.poi_accumulated.items():
            if points >= self.required_points:
                tokens.append(Token(owner=pubkey, amount=self.token_reward))
                block.poi_accumulated[pubkey] -= self.required_points
        return tokens

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
