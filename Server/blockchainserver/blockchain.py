import hashlib
import uuid
import json
from datetime import datetime
class blockchain:
    def __init__(self, current_node_url:str) -> None:
        self.chain = []
        self.pending_transactions = []
        self.create_new_block(100, '0', '0')
        self.current_node_url = current_node_url
        self.network_nodes = []
        self.drones = []

    # creates new block in the blockchain
    def create_new_block(self,nonce:int, previous_block_hash:str, hash:str):
        new_block = {
            'index' : len(self.chain) + 1,
            'timestamp' : str(datetime.now()),
            'transactions': self.pending_transactions,
            'nonce': nonce,
            'hash': hash,
            'previous_block_hash': previous_block_hash
        }
        self.pending_transactions = [];
        self.chain.append(new_block)
        return new_block
    
    # returns last block
    def get_last_block(self):
        return self.chain[len(self.chain) - 1]
    
    # creates new transaction
    def create_new_transaction(self, data:str, sender:str, recipient:str):
        new_transaction = {
            'data': data,
            'sender':sender,
            'recipient': recipient,
            'transaction_id': str(uuid.uuid4())
        }
        return new_transaction
    
    # adds newly created transactions to the pending transactions of all nodes
    def add_transaction_to_pending_transactions(self,transactionObj):
        self.pending_transactions.append(transactionObj)
        return self.get_last_block()['index'] + 1

    # creates a has for the perticular block
    def hash_block(self, previous_block_hash, current_block_data, nonce)-> str:
        data_as_string = previous_block_hash + str(nonce) + json.dumps(current_block_data)
        hash = hashlib.sha512(data_as_string.encode())
        return hash.hexdigest()

    # proof of work function to perform computation and generate nonce
    def proof_of_work(self,previous_block_hash:str, current_block_data)->int:
        nonce = 0
        hash = self.hash_block(previous_block_hash, current_block_data, nonce)
        while(str(hash).startswith('0000') != True):
            nonce += 1
            hash = self.hash_block(previous_block_hash, current_block_data, nonce)
        return nonce
    
    #checks if a given blockchain is valid or not
    def chain_is_valid(self, blockchain)-> bool:
        valid_chain = True
        for i in range(1, len(blockchain)):
            current_block = blockchain[i]
            prev_block = blockchain[i - 1]
            block_hash = self.hash_block(prev_block['hash'], {'transactions': current_block['transactions'], 'index': current_block['index']}, current_block['nonce'])
            if(block_hash.startswith('0000') !=True):
                valid_chain = False
            if(current_block['previous_block_hash'] != prev_block['hash']):
                valid_chain = False
        genesis_block = blockchain[0]
        correct_nonce = genesis_block['nonce'] == 100
        correct_previous_block_hash = genesis_block['previous_block_hash'] == '0'
        correct_hash = genesis_block['hash'] == '0'   
        correct_transactions = len(genesis_block['transactions'])== 0
        if not correct_nonce or not correct_previous_block_hash or not correct_hash or not correct_transactions:
            valid_chain = False
        return valid_chain