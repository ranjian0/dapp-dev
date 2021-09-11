deploy:
	python deploy.py --folder hello_world --network ganache

test:
	pytest hello_world/tests 
	
install-deps:
	pip install web3
	pip install py-solc-x
	pip install pytest

install-compiler:
	python -c "from solcx import install_solc; install_solc(version='latest')"