import hashlib
import uuid
import json
import sys
import requests_async as requests
from flask import jsonify, request
from blockchainserver import blockchain as bc
from blockchainserver import app
block_chain = bc.blockchain('http://'+sys.argv[1]+':'+sys.argv[2])
@app.route('/blockchain')
def blockchain():
    return jsonify({'chain': block_chain.chain,
        'pending_transactions': block_chain.pending_transactions,
        'current_node_url': block_chain.current_node_url,
        'network_nodes': block_chain.network_nodes,
        'drones': block_chain.drones})
@app.route('/add-drone', methods=['POST'])
def add_drone():
    data = request.get_json()
    drone_address = data['drone_address']
    block_chain.drones.append(drone_address)

@app.route('/remove-drone', methods=['POST'])
def remove_drone():
    data = request.get_json()
    drone_address = data['drone_address']
    block_chain.drones.pop(drone_address)
@app.route('/transaction', methods=['POST'])
def transaction():
    new_transaction = request.get_json()
    block_index = block_chain.add_transaction_to_pending_transactions(
    new_transaction)
    return jsonify({'note': f'trasaction will be added in block {block_index}.'})

@app.route('/mine', methods=['GET'])
async def mine():
    last_block = block_chain.get_last_block()
    previous_block_hash = last_block['hash']
    current_block_data ={
        'transactions':block_chain.pending_transactions,
        'index': last_block['index'] + 1
    }
    nonce = block_chain.proof_of_work(previous_block_hash, current_block_data)
    block_hash = block_chain.hash_block(previous_block_hash, current_block_data, nonce)
    new_block = block_chain.create_new_block(nonce, previous_block_hash, block_hash)
    for network_node_url in block_chain.network_nodes:
        await requests.post(url=network_node_url+'/recieve-new-block', json={'new_block': new_block})
    return jsonify({'note': 'new block mined successfully.', 'block': new_block})

@app.route('/recieve-new-block', methods=['POST'])
def recieve_new_block():
    data = request.get_json()
    new_block = data['new_block']
    last_block = block_chain.get_last_block()
    correct_hash = last_block['hash'] == new_block['previous_block_hash']
    correct_index = last_block['index'] + 1 == new_block['index']
    if correct_hash and correct_index:
        block_chain.chain.append(new_block)
        block_chain.pending_transactions = []
        return jsonify({'note': 'new block recieved and accepted', 'new_block': new_block})
    else:
        return jsonify({'note': 'new block rejected', 'new_block': new_block})

@app.route('/transaction/broadcast', methods=['POST'])
async def transaction_broacast():
    data = request.get_json()
    new_transaction = block_chain.create_new_transaction(data['data'], data['sender'], data['recipient'])
    block_chain.add_transaction_to_pending_transactions(new_transaction)
    for network_node_url in block_chain.network_nodes:
        await requests.post(url=network_node_url+'/transaction', json=new_transaction)
    return jsonify({'note': 'transaction created and broadcasted successfully'})

@app.route('/register-and-broadcast-node', methods=['POST'])
async def register_and_broadcast_nodes():
    data = request.get_json()
    new_node_url = data['new_node_url']
    if(block_chain.network_nodes.count(new_node_url) == 0):
        block_chain.network_nodes.append(new_node_url)
    for network_node_url in block_chain.network_nodes:
        data = {
            'new_node_url': new_node_url
        }
        await requests.post(url=network_node_url+'/register-node', json=data)
    
    all_nodes_data = block_chain.network_nodes.copy()
    all_nodes_data.append(block_chain.current_node_url)
    await requests.post(url=new_node_url+'/register-nodes-bulk', json={'all_network_nodes':all_nodes_data})
    return jsonify({'note': 'New node registered with network successfully.'})

@app.route('/register-nodes-bulk', methods=['POST'])
def register_nodes_bulk():
    data = request.get_json()
    all_network_nodes = data['all_network_nodes']
    for new_node_url in all_network_nodes:
        node_already_present = False
        if(block_chain.network_nodes.count(new_node_url) > 0):
            node_already_present = True
        not_current_node = block_chain.current_node_url != new_node_url
        if not node_already_present and not_current_node:
            block_chain.network_nodes.append(new_node_url)
    return jsonify({'note':'Bulk registration successful'})

@app.route('/register-node', methods=['POST'])
def register_nodes():
    data = request.get_json()
    new_node_url = data['new_node_url']
    node_already_present = False
    if(block_chain.network_nodes.count(new_node_url) > 0):
        node_already_present = True
    not_current_node = block_chain.current_node_url != new_node_url
    if not node_already_present and not_current_node:
        block_chain.network_nodes.append(new_node_url)
        return jsonify({'note': 'New node registered successfully.'})
    else:
        return jsonify({'note': 'New node not registered successfully.'})

@app.route('/consensus', methods=['GET'])
async def consensus():
    max_chain_length = len(block_chain.chain)
    new_longest_chain = None
    new_pending_transactions = None
    for network_node_url in block_chain.network_nodes:  # type: ignore
        neighbour_block_chain = await requests.get(url=network_node_url+'/blockchain')
        neighbour_block_chain = neighbour_block_chain.json()
        if len(neighbour_block_chain['chain']) > max_chain_length:
            max_chain_length = len(neighbour_block_chain['chain'])
            new_longest_chain = neighbour_block_chain['chain']
            new_pending_transactions = neighbour_block_chain['pending_transactions']
    if new_pending_transactions == None or (new_longest_chain != None and block_chain.chain_is_valid(new_longest_chain)):
        return jsonify({'note': 'Current chain has not been replaced.', 'chain':block_chain.chain})
    else:
        block_chain.chain = new_longest_chain
        block_chain.pending_transactions = new_pending_transactions
        return jsonify({'note': 'This chain has been replaced.', 'chain':block_chain.chain})
