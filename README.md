# Learning DAPP development 

## Environment setup

```
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ 
$ python -c "from solcx import install_solc; install_solc(version='latest')"
```

## Deploy a contract

```shell
$ python deploy.py --folder lottery --network ganache
```

requires evironment variable GANACHE_URL to be set e.g to http://127.0.0.1:7545

## Run some tests

```shell
$ pytest lottery/tests
```