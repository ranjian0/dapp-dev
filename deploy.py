import os
import json
import argparse
from pathlib import Path

from web3 import Web3
from solcx import compile_files

CURDIR = Path(__file__).parent.absolute()


def get_web3(network):
    if network == "ganache":
        return Web3(Web3.HTTPProvider(os.getenv("GANACHE_URL")))
    return None


def main():
    # Create the parser
    parser = argparse.ArgumentParser(description='Deploy Ethereum Smart Contract')

    parser.add_argument('--folder', type=str, required=True,
        help="Folder containing a 'contracts' subfolder with solidity files")

    parser.add_argument('--network', type=str, required=True,
        choices=["mainnet", "ropsten", "ganache"],
        help="Network to deploy the contract to e.g 'mainnet' for ethereum main network")

    args = parser.parse_args()

    deploy_network = args.network
    smart_contracts_folder = Path(args.folder).absolute() / "contracts"

    if not smart_contracts_folder.exists():
        print(f"{str(smart_contracts_folder)} does not exist!")
        return
    
    sol_files = list(smart_contracts_folder.glob("**/*.sol"))
    compiled_contracts = compile_files(sol_files)

    w3 = get_web3(deploy_network)
    for contract_key, contract_interface in compiled_contracts.items():
        # Instantiate and deploy contract
        contract = w3.eth.contract(
            abi=contract_interface['abi'], bytecode=contract_interface['bin'])

        deploy_params = {'from': w3.eth.accounts[1]}
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


if __name__ == "__main__":
    main()