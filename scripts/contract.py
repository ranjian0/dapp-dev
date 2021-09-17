import os
import json
from web3 import Web3
from pathlib import Path
from solcx import compile_files 


class Contract:

    def __init__(self, folder):
        norm_path = os.path.normpath(folder)
        smart_contracts_folder = Path(norm_path).absolute() / "contracts"

        if not smart_contracts_folder.exists():
            raise ValueError(f"{str(smart_contracts_folder)} does not exist!")
        
        sol_files = list(smart_contracts_folder.glob("**/*.sol"))
        self.compiled_contracts = compile_files(sol_files)


    def deploy(self, chain):
        w3 = Contract.web3(chain)
        if not w3.isConnected():
            raise ValueError("Connection failed!")

        if chain == "ganache":
            # XXX Local deployment
            self.deploy_local(w3)
            return

        # Deploy to network

        account = w3.eth.account.privateKeyToAccount(os.getenv('PRIVATE_KEY'))
        balance = w3.eth.get_balance(account.address)
        print(f"Account Balance for {account.address}: \n", Web3.fromWei(balance, 'ether'), 'ether')

        deploy_params = {
            'from': account.address,
            'nonce': w3.eth.get_transaction_count(account.address),
            'gas': 1720000,
            'gasPrice': w3.toWei(21, 'gwei')
        }
        for contract_key, contract_interface in self.compiled_contracts.items():
            # Instantiate and deploy contract
            contract = w3.eth.contract(
                abi=contract_interface['abi'], bytecode=contract_interface['bin'])

            deployment_estimate = contract.constructor().estimateGas(transaction=deploy_params)
            contract_txn = contract.constructor().buildTransaction(deploy_params)
            signed = account.signTransaction(contract_txn)
            tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)        
            contract_address = tx_hash.hex()

            print(f"Deployed {contract_key} \n\tto: {contract_address} \n\tusing: {deployment_estimate} gas.")

            # -- save out the address and abi for usage later
            contract_fp, filename = contract_key.split(':')
            save_file = Path(contract_fp).parent.parent.absolute() / "build" / f"{filename}.json"
            save_file.parent.mkdir(parents=True, exist_ok=True)
            data = {
                "abi": contract_interface['abi'],
                "contract_address": contract_address
            }
            with open(save_file, 'w') as sf:
                json.dump(data, sf, indent=4, sort_keys=True)
            print(f"Contract saved to {save_file}")
        
        
    def deploy_local(self, w3):
        deploy_params = {
            'from': w3.eth.accounts[0],
            'gas': 1720000,
            'gasPrice': w3.toWei(21, 'gwei')
        }
        for contract_key, contract_interface in self.compiled_contracts.items():
            # Instantiate and deploy contract
            contract = w3.eth.contract(
                abi=contract_interface['abi'], bytecode=contract_interface['bin'])

            deployment_estimate = contract.constructor().estimateGas(transaction=deploy_params)

            # Get transaction hash from deployed contract
            tx_hash = contract.constructor().transact(transaction=deploy_params)
            tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
            contract_address = tx_receipt['contractAddress']

            print(f"Deployed {contract_key} \n\tto: {contract_address} \n\tusing: {deployment_estimate} gas.")

            # -- save out the address and abi for usage later
            contract_fp, filename = contract_key.split(':')
            save_file = Path(contract_fp).parent.parent.absolute() / "build" / f"{filename}.json"
            save_file.parent.mkdir(parents=True, exist_ok=True)
            data = {
                "abi": contract_interface['abi'],
                "contract_address": contract_address
            }
            with open(save_file, 'w') as sf:
                json.dump(data, sf, indent=4, sort_keys=True)
            print(f"Contract saved to {save_file}")


    @staticmethod
    def web3(chain):
        if chain == "ganache":
            return Web3(Web3.HTTPProvider(os.getenv("GANACHE_URL")))
        elif chain == "mainnet":
            return Web3(Web3.HTTPProvider(f"https://mainnet.infura.io/v3/{os.getenv('WEB3_INFURA_PROJECT_ID')}"))
        elif chain == "ropsten":
            return Web3(Web3.HTTPProvider(f"https://ropsten.infura.io/v3/{os.getenv('WEB3_INFURA_PROJECT_ID')}"))
        elif chain == "rinkeby":
            return Web3(Web3.HTTPProvider(f"https://rinkeby.infura.io/v3/{os.getenv('WEB3_INFURA_PROJECT_ID')}"))
        return None

