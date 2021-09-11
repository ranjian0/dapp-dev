import os
import json
import pytest
from pathlib import Path 

from web3 import Web3

CONTRACT = Path(__file__).parent.parent.absolute() / "build" / "HelloWorld.json"


@pytest.fixture
def w3():
    w3 = Web3(Web3.HTTPProvider(os.getenv("GANACHE_URL"))) 
    w3.eth.default_account = w3.eth.accounts[1]
    return w3

@pytest.fixture
def contract(w3):
    with open(CONTRACT, 'r') as f:
        data = json.load(f)

    return w3.eth.contract(
        abi=data["abi"],
        address=data["contract_address"], 
    )


def test_hello(contract, w3):
    tx_hash = contract.functions.set_greeting("Hello, World")
    tx_hash = tx_hash.transact()
    w3.eth.wait_for_transaction_receipt(tx_hash)

    assert contract.functions.get_greeting().call() == "Hello, World"


    tx_hash = contract.functions.set_greeting("Hello, Ian")
    tx_hash = tx_hash.transact()
    w3.eth.wait_for_transaction_receipt(tx_hash)

    assert contract.functions.get_greeting().call() == "Hello, Ian"
