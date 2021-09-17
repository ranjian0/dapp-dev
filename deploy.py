import argparse
from scripts.contract import Contract

def main():
    # Create the parser
    parser = argparse.ArgumentParser(description='Deploy Ethereum Smart Contract')

    parser.add_argument('--folder', type=str, required=True,
        help="Folder containing a 'contracts' subfolder with solidity files")

    parser.add_argument('--chain', type=str, required=True,
        choices=["ganache", "mainnet", "ropsten", "rinkeby"],
        help="Chain to deploy the contract to e.g 'mainnet' for ethereum main network")

    args = parser.parse_args()

    contract = Contract(args.folder)
    contract.deploy(args.chain)

if __name__ == "__main__":
    main()