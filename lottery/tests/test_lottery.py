import os
import json
import pytest
from pathlib import Path 

from web3 import Web3

CONTRACT = Path(__file__).parent.parent.absolute() / "build" / "Lottery.json"


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


def test_lottery(contract, w3):
    player_accounts = [
        account for account in w3.eth.accounts 
        if account != w3.eth.default_account and w3.eth.get_balance(account) > 0
    ]

    balances = list(map(w3.eth.get_balance, player_accounts))
    assert all(b > 0 for b in balances)

    # -- add some new players
    for account in player_accounts:
        if w3.eth.get_balance(account) > w3.toWei(0.0001, 'ether'):
            tx_hash = contract.functions.enter()
            tx_hash = tx_hash.transact({'from':account, 'value':str(w3.toWei(0.0001, 'ether'))})
            w3.eth.wait_for_transaction_receipt(tx_hash)

    assert contract.functions.get_balance().call() > 0

    # -- pick winner
    tx_hash = contract.functions.pick_winner()
    tx_hash = tx_hash.transact({'from':w3.eth.default_account})
    w3.eth.wait_for_transaction_receipt(tx_hash)

    assert contract.functions.get_balance().call() == 0

    
