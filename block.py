import hashlib
import time


class Block:
    def __init__(self, index, previous_hash, interactions, timestamp=None):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp or time.time()
        self.interactions = interactions
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_data = str(self.index) + self.previous_hash + str(self.timestamp) + "".join(
            [interaction.signature.hex() for interaction in self.interactions])
        return hashlib.sha256(block_data.encode("utf-8")).hexdigest()
