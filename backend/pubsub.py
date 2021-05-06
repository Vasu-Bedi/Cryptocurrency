import time
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
from backend.blockchain.Block import Block
from backend.wallet.transaction import Transaction

pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-20408ed6-a4a8-11eb-86bf-e27ecfa4e4f1'
pnconfig.publish_key = 'pub-c-f6286079-5cd7-46aa-b3c2-c6d849b33700'

CHANNELS = {
    'TEST' : 'TEST',
    'BLOCK' : 'BLOCK',
    'TRANSACTION' : 'TRANSACTION'
}

class Listener(SubscribeCallback):
    def __init__(self, blockchain, transaction_pool):
        self.blockchain = blockchain
        self.transaction_pool = transaction_pool

    def message(self, pubnub, message_object):
        print(f'\n-- Channel: {message_object.channel} | Message: {message_object.message}')

        if message_object.channel == CHANNELS['BLOCK']:
            block = Block.from_json(message_object.message)
            potential_chain = self.blockchain.chain[:]
            potential_chain.append(block)
            try:
                self.blockchain.replace_chain(potential_chain)
                print('\n --Successfully replaced the local chain')
            except Exception as e:
                print(f'\n --Did not replace chain: {e}')

        elif message_object.channel == CHANNELS['TRANSACTION']:
            transaction = Transaction.from_json(message_object.message)
            self.transaction_pool.set_transaction(transaction)
            print('\n -- Set the new transaction in the transaction pool.')

class PubSub():
    '''
    Handles the publish/Subscribe layer of application
    Provides communication bw nodes of a blockchain network
    '''
    def __init__(self, blockchain, transaction_pool):
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute() # Sends a request to online pubnub application that this object is now subscribed to this channel
        self.pubnub.add_listener(Listener(blockchain, transaction_pool))

    def publish(self, channel, message):
        self.pubnub.publish().channel(channel).message(message).sync() # Send the message to all subscribers

    def broadcast_block(self, block):
        '''
        Broadcast a block object to all nodes
        '''
        self.publish(CHANNELS['BLOCK'], block.to_json())
    
    def broadcast_transaction(self, transaction):
        """
        Broadcast a transaction to all nodes.
        """
        self.publish(CHANNELS['TRANSACTION'], transaction.to_json())

def main():
    pubsub = PubSub(blockchain)
    time.sleep(1)
    pubsub.publish(CHANNELS['TEST'], {'foo': 'bar'})
    
if __name__ == '__main__':
    main()