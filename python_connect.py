import json
import web3

from web3 import Web3, HTTPProvider, IPCProvider
from solc import compile_source
from web3.contract import ConciseContract

# Solidity source code
contract_source_code = '''
pragma solidity ^0.4.0;

contract Greeter {
    string public greeting;

    function Greeter() {
        greeting = 'Hello';
    }

    function setGreeting(string _greeting) public {
        greeting = _greeting;
    }

    function greet() constant returns (string) {
        return greeting;
    }
}
'''

compiled_sol = compile_source(contract_source_code) # Compiled source code
contract_interface = compiled_sol['<stdin>:Greeter']

# web3.py instance
# Change your IP address and Port to your instance
w3 = Web3(HTTPProvider('http://35.198.20.187:8000'))

# Instantiate and deploy contract
contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

# Get transaction hash from deployed contract
tx_hash = contract.deploy(transaction={'from': w3.eth.accounts[0], 'gas': 410000})

# Get tx receipt to get contract address
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

contract_address = tx_receipt['contractAddress']

# Contract instance in concise mode
abi = contract_interface['abi']
contract_instance = w3.eth.contract(address=contract_address, abi=abi,ContractFactoryClass=ConciseContract)

# Getters + Setters for web3.eth.contract object
print('Contract value Initially: {}'.format(contract_instance.greet()))
a = contract_instance.setGreeting('Yashwanth', transact={'from': w3.eth.accounts[0]})
print(a.hex())
b = w3.eth.waitForTransactionReceipt(a)

print('Setting value to: Yashwanth')
print('Contract value: {}'.format(contract_instance.greet()))
