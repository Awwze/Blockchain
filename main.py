import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

def calculate_hash(index, previous_hash, timestamp, data):
    value = f"{index}{previous_hash}{timestamp}{data}"
    return hashlib.sha256(value.encode('utf-8')).hexdigest()

def create_genesis_block():
    # Генезис блок — первый блок в блокчейне
    return Block(0, "0", int(time.time()), "Genesis Block",
                 calculate_hash(0, "0", int(time.time()), "Genesis Block"))

def create_new_block(previous_block, data):
    index = previous_block.index + 1
    timestamp = int(time.time())
    previous_hash = previous_block.hash
    new_hash = calculate_hash(index, previous_hash, timestamp, data)
    return Block(index, previous_hash, timestamp, data, new_hash)

class Blockchain:
    def __init__(self):
        self.chain = [create_genesis_block()]

    def add_block(self, data):
        previous_block = self.chain[-1]
        new_block = create_new_block(previous_block, data)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != calculate_hash(current_block.index,
                                                   current_block.previous_hash,
                                                   current_block.timestamp,
                                                   current_block.data):
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

# Пример использования
blockchain = Blockchain()

# Добавляем новые блоки
blockchain.add_block("Transaction Data 1")
blockchain.add_block("Transaction Data 2")

# Проверка целостности блокчейна
print("Blockchain valid:", blockchain.is_chain_valid())

# Выводим информацию о блоках
for block in blockchain.chain:
    print(f"Block {block.index} [Previous Hash: {block.previous_hash}]")
    print(f"Data: {block.data}")
    print(f"Hash: {block.hash}\n")
