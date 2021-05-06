from backend.blockchain.Block import Block

class Blockchain:
    def __init__(self):
        self.chain = [Block.genesis()]

    def add_block(self, data):
        self.chain.append(Block.mine_block(self.chain[-1], data))

    def __repr__(self):
        return f"Blockchain : {self.chain}"

    def replace_chain(self, chain):
        '''
        Replace the local chain with incoming one if following rules apply
        - The incoming chain must be longer than local one
        - The incoming chain is formatted properly
        '''
        if len(chain)<=len(self.chain):
            raise Exception('Cannot Replace. The incoming chain must be longer')
        try:
            Blockchain.is_valid_chain(chain)
        except Exception as e:
            raise Exception(f'Cannot Replace. The incoming chain is invalid: {e}')
        self.chain = chain # If no error occurs above, we replace the chain

    def to_json(self):
        # Serialize the blockchain into a list of blocks
        return list(map(lambda block: block.to_json(), self.chain))

    @staticmethod
    def from_json(chain_json):
        '''
        Deserialize a list of serialised blocks into Blockchain object or a chain of Block instances
        '''
        blockchain = Blockchain()
        blockchain.chain = list(map(lambda block_json: Block.from_json(block_json), chain_json))
        return blockchain


    @staticmethod
    def is_valid_chain(chain):
        '''
        Validate the blockchain using following rules
        - chain must start with genesis block
        - blocks must be formatted correctly
        '''
        if chain[0].__dict__ != Block.genesis().__dict__: # Python can't check equality of two objects, but dictionaries
            raise Exception('The genesis block must be valid')    

        for i in range(1, len(chain)):
            block = chain[i]
            last_block = chain[i-1]
            Block.is_valid_block(last_block, block)


def main():
    blockchain = Blockchain()
    blockchain.add_block('one')
    blockchain.add_block('two')

    print(blockchain)
    print(f"blockchain.py __name__ : {__name__}")

if __name__ == '__main__':
    main()