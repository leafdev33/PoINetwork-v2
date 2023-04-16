from block import Block


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "0", [], 0)

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, interactions):
        index = len(self.chain)
        previous_hash = self.get_last_block().hash
        new_block = Block(index, previous_hash, interactions)
        self.chain.append(new_block)
