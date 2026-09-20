import hashlib
import time
from datetime import datetime, timezone

class Block:
    def __init__(self, index, data, prev_hash):
        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.prev_hash = prev_hash
        self.hash = self.calculate_hash()

    @property
    def timestamp_readable(self):
        local_tz = datetime.now().astimezone().tzinfo
        dt = datetime.fromtimestamp(self.timestamp, tz=local_tz)
        return dt.astimezone().strftime( "%Y-%m-%d %H:%M:%S %Z" )

    def calculate_hash(self):

        block_string = str(self.index) + str(self.timestamp) + str(self.data) + str(self.prev_hash)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(1, "Genesis Block (Awal Mula)", "0")
        self.chain.append(genesis_block)

    def add_block(self, data):
        last_block = self.chain[-1]
        new_block = Block(last_block.index + 1, data, last_block.hash)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.prev_hash != previous_block.hash:
                return False
        return True